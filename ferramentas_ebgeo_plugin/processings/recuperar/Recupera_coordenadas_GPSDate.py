from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFile,
    QgsProcessingParameterVectorDestination,
    QgsProcessingParameterDateTime,
    QgsVectorLayer,
    QgsFields,
    QgsField,
    QgsFeature,
    QgsPointXY,
    QgsGeometry,
    QgsVectorFileWriter
)
from PyQt5.QtCore import QVariant, QDateTime
import os, json
from datetime import timedelta

class RecuperarCoordenadasMetadadoGPSDate(QgsProcessingAlgorithm):

    INPUT_JSON_FOLDER = 'INPUT_JSON_FOLDER'
    INPUT_IMG_FOLDER = 'INPUT_IMG_FOLDER'
    INPUT_START_DATETIME = 'INPUT_START_DATETIME'
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
            QgsProcessingParameterDateTime(
                self.INPUT_START_DATETIME,
                'Data/Hora inicial'
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(
                self.OUTPUT,
                'Camada de saída'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        json_folder = self.parameterAsFile(parameters, self.INPUT_JSON_FOLDER, context)
        img_folder = self.parameterAsFile(parameters, self.INPUT_IMG_FOLDER, context)
        start_qdatetime: QDateTime = self.parameterAsDateTime(parameters, self.INPUT_START_DATETIME, context)
        output_path = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)

        # Converter para datetime Python
        current_time = start_qdatetime.toPyDateTime()

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
        for file in sorted(os.listdir(json_folder)):
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

            feat = QgsFeature()
            feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(lon, lat)))
            feat.setAttributes([
                camera.get('id'),
                camera.get('img') + '.jpg',
                lon,
                lat,
                float(camera.get('ele', 0)),
                float(camera.get('heading', 0)),
                current_time.strftime("%Y-%m-%d %H:%M:%S")
            ])
            provider.addFeatures([feat])

            # Incrementar 10 segundos
            current_time += timedelta(seconds=10)

        layer.updateExtents()

        # Salvar como GeoPackage
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = "GPKG"
        QgsVectorFileWriter.writeAsVectorFormatV2(layer, output_path, context.transformContext(), options)

        return {self.OUTPUT: output_path}

    def name(self):
        return 'recuperar_coordenadas_metadado_gpsdate'

    def displayName(self):
        return '2.1 Recuperar coordenadas do metadado - GPSDate'

    def group(self):
        return 'Recuperar imagens'

    def groupId(self):
        return 'recuperar'

    def createInstance(self):
        return RecuperarCoordenadasMetadadoGPSDate()
