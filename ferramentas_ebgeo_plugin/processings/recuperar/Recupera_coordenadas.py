from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFile,
    QgsProcessingParameterVectorDestination,
    QgsVectorLayer,
    QgsFields,
    QgsField,
    QgsFeature,
    QgsPointXY,
    QgsGeometry,
    QgsWkbTypes,
    QgsVectorFileWriter
)
from PyQt5.QtCore import QVariant
import os, json
from PIL import Image
from PIL.ExifTags import TAGS

class RecuperarCoordenadasMetadado(QgsProcessingAlgorithm):

    INPUT_JSON_FOLDER = 'INPUT_JSON_FOLDER'
    INPUT_IMG_FOLDER = 'INPUT_IMG_FOLDER'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_JSON_FOLDER,
                'Pasta com arquivos JSON',
                behavior=QgsProcessingParameterFile.Folder
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_IMG_FOLDER,
                'Pasta com imagens',
                behavior=QgsProcessingParameterFile.Folder
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(
                self.OUTPUT,
                'Camada de saída'
            )
        )

    def get_exif_datetime(self, image_path):
        try:
            img = Image.open(image_path)
            exif_data = img._getexif()
            if not exif_data:
                return None

            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == 'DateTimeOriginal':
                    return value  # formato 'YYYY:MM:DD HH:MM:SS'
        except Exception:
            return None
        return None

    def processAlgorithm(self, parameters, context, feedback):
        json_folder = self.parameterAsFile(parameters, self.INPUT_JSON_FOLDER, context)
        img_folder = self.parameterAsFile(parameters, self.INPUT_IMG_FOLDER, context)
        output_path = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)

        # Definir campos da camada
        fields = QgsFields()
        fields.append(QgsField('id', QVariant.String))
        fields.append(QgsField('img', QVariant.String))
        fields.append(QgsField('lon', QVariant.Double))
        fields.append(QgsField('lat', QVariant.Double))
        fields.append(QgsField('ele', QVariant.Double))
        fields.append(QgsField('heading', QVariant.Double))
        fields.append(QgsField('GPSTime', QVariant.String))

        layer = QgsVectorLayer('Point?crs=EPSG:4326', 'coordenadas', 'memory')
        provider = layer.dataProvider()
        provider.addAttributes(fields)
        layer.updateFields()

        # Iterar sobre os arquivos JSON
        for file in os.listdir(json_folder):
            if not file.lower().endswith('.json'):
                continue

            filepath = os.path.join(json_folder, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            camera = data.get('camera', {})
            if not camera:
                continue

            lon = float(camera.get('lon', 0))
            lat = float(camera.get('lat', 0))

            # Buscar a imagem correspondente
            img_name = os.path.join(camera.get('img')+ '.jpg')
            img_path = os.path.join(img_folder, img_name)

            gps_time = None
            if os.path.exists(img_path):
                gps_time = self.get_exif_datetime(img_path)

            feat = QgsFeature()
            feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(lon, lat)))
            feat.setAttributes([
                camera.get('id'),
                camera.get('img')+'.jpg',
                float(camera.get('lon', 0)),
                float(camera.get('lat', 0)),
                float(camera.get('ele', 0)),
                float(camera.get('heading', 0)),
                gps_time
            ])
            provider.addFeatures([feat])

        layer.updateExtents()

        # Salvar como GeoPackage
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = "GPKG"
        QgsVectorFileWriter.writeAsVectorFormatV2(layer, output_path, context.transformContext(), options)

        return {self.OUTPUT: output_path}

    def name(self):
        return 'recuperar_coordenadas_metadado'

    def displayName(self):
        return '2. Recuperar coordenadas do metadado'

    def group(self):
        return 'Recuperar imagens'

    def groupId(self):
        return 'recuperar'

    def createInstance(self):
        return RecuperarCoordenadasMetadado()
