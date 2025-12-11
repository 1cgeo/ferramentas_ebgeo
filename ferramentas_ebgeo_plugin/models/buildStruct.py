import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from qgis.core import (
    QgsGeometry,
    QgsPointXY,
    QgsDistanceArea,
    QgsProject,
    QgsVectorLayer,
    QgsRendererCategory,
    QgsSymbol,
    QgsCategorizedSymbolRenderer,
    QgsSimpleLineSymbolLayer,
    QgsLineSymbol,
    QgsSpatialIndex, 
    QgsFeature,
    QgsSimpleFillSymbolLayer,
    QgsWkbTypes
)
import os
import processing
import random
from .camera import CameraImage, CameraFactory
from pyproj import Geod
import numpy as np
geod = Geod(ellps="WGS84")


class BuildStruct:

    def build(self, imagesFolderPath):
        images = self.loadImagesDataset(imagesFolderPath)
        images.columns = ['{}_img'.format(name) for name in images.columns]
        
        csvImagesPath = self.getCsvImagesPath()
        images.to_csv(csvImagesPath, index=False)
        self.loadCSVLayer(csvImagesPath, 'todas_imagens')

        result = self.removeDuplicatePoints(images)
        result = self.removeDuplicateLines(result)
        result = self.createLines(result)
        result = self.removeNearPoints(result)
        csvStructPath = self.getCsvStructPath()
        result.to_csv(csvStructPath, index=False)
        outputLayer = self.loadCSVLayer(csvStructPath, 'imagens_processadas')
        self.applyStyles(outputLayer)
        self.buildLineGeometries(csvStructPath)  
        

    def loadImagesDataset(self, imagesFolderPath):
        images = []

        def process_image(filename):
            if not filename.endswith('.jpg'):
                return None
            imagePath = os.path.join(imagesFolderPath, filename)
            image = CameraFactory.from_image(imagePath)
            if not image: 
                return None
            lon, lat, ele = image.getLongLatAlt()
            year, month, day = image.getYearMonthDay()
            hour, minute, second = image.getHourMinuteSecond()
            imageNumber = image.getImageNumber()
            imageRange = image.getImageRange()
            imageName = image.getImageName()
            meshRotationY = image.getMeshRotationY()
            return [
                imageRange,
                imageNumber,
                imageName,
                datetime(int(year), int(month), int(day), int(hour), int(minute), int(second)).timestamp(),
                lon, 
                lat, 
                ele,
                meshRotationY
            ]

        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = [executor.submit(process_image, f) for f in os.listdir(imagesFolderPath)]
            for fut in as_completed(futures):
                result = fut.result()
                if result:
                    images.append(result)

        imagesDF = pd.DataFrame(images, columns=['faixa','numero','nome','time','long','lat','ele', 'mesh_rotation_y'])
        imagesDF["time"] = imagesDF["time"].astype(int)
        return imagesDF
    
    def removeDuplicatePoints(self, points):
        points_cleaned  = points.drop_duplicates(subset=['long_img', 'lat_img'], keep='first')
        return points_cleaned 

    def removeDuplicateLines(self, dataset):
        points = []
        deleteImages = {}

        groupSorted = dataset.sort_values(['faixa_img', 'numero_img']).reset_index(drop=True)

        features = []
        index = QgsSpatialIndex()
        for i, row in groupSorted.iterrows():
            feat = QgsFeature()
            geom = QgsGeometry.fromPointXY(QgsPointXY(row['long_img'], row['lat_img']))
            feat.setGeometry(geom)
            feat.setId(i)
            features.append((i, row, geom))
            index.addFeature(feat)

        for idxA, rowA, geomA in features:
            if rowA['faixa_img'] in deleteImages and rowA['numero_img'] in deleteImages[rowA['faixa_img']]:
                continue

            points.append(rowA.to_dict())

            bufferA = geomA.buffer(0.00010, 5)
            nearby_ids = index.intersects(bufferA.boundingBox()) 

            for idxB in nearby_ids:
                if idxB <= idxA:
                    continue

                rowB = groupSorted.iloc[idxB]
                if abs(rowA["time_img"] - rowB["time_img"]) <= 5:
                    continue

                geomB = features[idxB][2]
                if not bufferA.intersects(geomB):
                    continue

                deleteImages.setdefault(rowB['faixa_img'], []).append(rowB['numero_img'])

        return pd.DataFrame(points, columns=[name for name in dataset.columns.to_list()])

    def distance(self, point1, point2):
        distance = QgsDistanceArea()
        distance.setEllipsoid('WGS84')
        return distance.measureLine(point1, point2)
    
    def createLines(self, dataset):
        dataset = dataset.sort_values('time_img').reset_index(drop=True)
        n = len(dataset)
        if n < 2:
            return dataset

        lons = dataset['long_img'].to_numpy()
        lats = dataset['lat_img'].to_numpy()

        dist = self.computeDistances(lons, lats)

        faixa_idx = np.zeros(n, dtype=int)
        line_idx = 0

        for i in range(1, n):
            if dist[i - 1] > 40:
                line_idx += 1
            faixa_idx[i] = line_idx

        dataset['faixa_img'] = faixa_idx

        counts = np.bincount(faixa_idx)
        valid_faixas = np.where(counts >= 2)[0]
        dataset = dataset[dataset['faixa_img'].isin(valid_faixas)]

        return dataset
    
    def computeDistances(self, lons, lats):
        chunks = np.array_split(np.arange(len(lons) - 1), os.cpu_count())

        def compute_chunk(indices):
            lon1 = lons[indices]
            lat1 = lats[indices]
            lon2 = lons[indices + 1]
            lat2 = lats[indices + 1]
            _, _, dist = geod.inv(lon1, lat1, lon2, lat2)
            return dist

        with ThreadPoolExecutor() as executor:
            results = executor.map(compute_chunk, chunks)

        return np.concatenate(list(results))
    
    def getCsvImagesPath(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 
            '..',
            'tmp',
            'STRUCT.csv'
        )

    def getCsvStructPath(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 
            '..',
            'tmp',
            'STRUCT.csv'
        )

    def buildFillStyle(self, count):
        fills = []
        for _ in range(count):
            layer_style = {}
            layer_style['color'] = '%d, %d, %d' % (random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))
            layer_style['outline'] = '#000000'
            fills.append( QgsSimpleFillSymbolLayer.create(layer_style) )
        return fills

    def loadCSVLayer(self, csvPath, layerName):
        uri = "file:///{}?type='csv&maxFields=10000&detectTypes=yes&xField=long_img&yField=lat_img&crs=EPSG:4326&spatialIndex=no&subsetIndex=no&watchFile=no'".format(
            csvPath
        )
        layer = QgsVectorLayer(uri, layerName, 'delimitedtext')
        geom_type = QgsWkbTypes.displayString(layer.wkbType())
        outLayer = QgsVectorLayer(f"{geom_type}?crs={layer.crs().authid()}", layerName, "memory")
        prov = outLayer.dataProvider()
        prov.addAttributes(layer.fields())
        outLayer.updateFields()
        for feat in layer.getFeatures():
            outFeat = QgsFeature(layer.fields())
            outFeat.setAttributes(feat.attributes())
            outFeat.setGeometry(feat.geometry())
            prov.addFeature(outFeat)
        QgsProject.instance().addMapLayer(outLayer)
        return outLayer

    def applyStyles(self, layer):
        fni = layer.dataProvider().fieldNameIndex('faixa_img')
        uniqueValues = layer.uniqueValues(fni)
        fills = self.buildFillStyle( len(uniqueValues) )
        categories = []
        for idx, uniqueValue in enumerate(uniqueValues):
            symbol = QgsSymbol.defaultSymbol(layer.geometryType())
            symbolLayer = fills[idx]
            if symbolLayer is not None:
                symbol.changeSymbolLayer(0, symbolLayer)
            category = QgsRendererCategory(uniqueValue, symbol, str(uniqueValue))
            categories.append(category)
        renderer = QgsCategorizedSymbolRenderer('faixa_img', categories)
        if renderer is not None:
            layer.setRenderer(renderer)
        layer.triggerRepaint()

    def removeNearPoints(self, dataset: pd.DataFrame):
        columns = dataset.columns.to_list()
        groupSorted = dataset.sort_values(['faixa_img', 'numero_img']).reset_index(drop=True)
        n = len(groupSorted)
        if n == 0:
            return dataset

        features = []
        for i, row in groupSorted.iterrows():
            feat = QgsFeature()
            feat.setId(i)
            feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(row['long_img'], row['lat_img'])))
            feat.setAttributes(row.to_list())
            features.append(feat)

        spatial_index = QgsSpatialIndex()
        for feat in features:
            spatial_index.addFeature(feat)

        points = []
        deleteImages = {}

        for idxA, rowA in groupSorted.iterrows():
            faixa = rowA['faixa_img']
            num = rowA['numero_img']

            if faixa in deleteImages and num in deleteImages[faixa]:
                continue

            points.append(rowA.to_list())

            if faixa not in deleteImages:
                deleteImages[faixa] = set()

            geomA = features[idxA].geometry()
            bufferA = geomA.buffer(0.00010, 5)

            candidate_ids = spatial_index.intersects(bufferA.boundingBox())

            for idxB in candidate_ids:
                if idxB <= idxA:
                    continue
                rowB = groupSorted.iloc[idxB]

                if rowB['faixa_img'] != faixa:
                    continue

                geomB = features[idxB].geometry()
                if bufferA.intersects(geomB):
                    deleteImages[faixa].add(rowB['numero_img'])

        return pd.DataFrame(points, columns=columns)
    
    def random_color(self):
        return '#{:06x}'.format(random.randint(0, 0xFFFFFF))
    
    def buildLineStyle(self, count):
        lines = []
        for _ in range(count):
            layer_style = {}
            layer_style['color'] = '%d, %d, %d' % (random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))
            layer_style['width'] = '1'
            lines.append( QgsSimpleLineSymbolLayer.create(layer_style) )
        return lines
    
    def styleLineLayer(self, layer:QgsVectorLayer, fieldName="faixa_img", width=1.0):
        if not layer:
            return
        else:            
            fni = layer.dataProvider().fieldNameIndex(fieldName)
            unique_values = layer.uniqueValues(fni)
            lineStyle = self.buildLineStyle( len(unique_values) )
            
            categories = []
            symbolLine = QgsSymbol.defaultSymbol(layer.geometryType())
            if symbolLine is None:
                color = self.random_color()
                symbolLine = QgsLineSymbol.createSimple({'color': color.name(), 'width': str(width)})
            if symbolLine.symbolLayer(0):
                symbolLine.symbolLayer(0).setWidth(width)
            
            for idx, value in enumerate(unique_values):
                symbolLayer = lineStyle[idx]
                if symbolLayer is not None:
                    symbolLine.changeSymbolLayer(0, symbolLayer)
                    symbolLine2 = QgsLineSymbol.createSimple({'color': self.random_color(), 'width': '1'})
                
                    categoryLine = QgsRendererCategory()
                    categoryLine.setValue(value)
                    categoryLine.setSymbol(symbolLine2)
                    categoryLine.setLabel(str(value))
                    categories.append(categoryLine)
            
            renderer = QgsCategorizedSymbolRenderer(fieldName, categories)
            
            if renderer is not None:
                layer.setRenderer(renderer)
            
            layer.triggerRepaint()

    def buildLineGeometries(self, csvPath)->QgsVectorLayer:
        layer = processing.run(
            'native:pointstopath', 
             { 
                    'CLOSE_PATH' : False, 
                    'GROUP_EXPRESSION' : '"faixa_img"', 
                    'INPUT' : 'delimitedtext://file:///{}?type=csv&maxFields=10000&detectTypes=yes&xField=long_img&yField=lat_img&crs=EPSG:4326&spatialIndex=no&subsetIndex=no&watchFile=no'.format(csvPath), 
                    'NATURAL_SORT' : False, 
                    'ORDER_EXPRESSION' : '"time_img"', 
                    'OUTPUT' : 'TEMPORARY_OUTPUT' 
            }
        )['OUTPUT']
        layer.startEditing()
        layer.setName('conexao')
        layer.commitChanges()

        QgsProject.instance().addMapLayer(layer)
        self.styleLineLayer(layer, fieldName='faixa_img', width=1)