"""
/***************************************************************************
 Imagens para pontos
                                 A QGIS plugin
 Conjunto de ferramentas do Streetview do 1° CGEO.
                              -------------------
        begin                : 2024-11-26
        copyright            : (C) 2024 by Brazilian Army Cartographic
 ***************************************************************************/
"""

__author__ = '1° Ten Raul Magno / 1° CGEO'
__date__ = '2025-04-17'
__copyright__ = '(C) 2024 by Brazilian Army Cartographic Tools'


from qgis.core import (
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsProcessingAlgorithm,
    QgsVectorLayer,
    QgsField,
    QgsFields,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsProject,
    QgsProcessingException,
    QgsVectorFileWriter,
    QgsWkbTypes,
    QgsCoordinateReferenceSystem,
)
from PyQt5.QtCore import QVariant
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import re


class ImageToGeometry(QgsProcessingAlgorithm):
    PASTA = 'PASTA'
    SAIDA = 'SAIDA'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile(
                self.PASTA,
                'Pasta contendo as imagens',
                behavior=QgsProcessingParameterFile.Folder,
                defaultValue=None
            )
        )
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.SAIDA,
                'Arquivo de saída base (GeoPackage)',
                fileFilter='GeoPackage (*.gpkg)'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        pasta_raiz = self.parameterAsFile(parameters, self.PASTA, context)
        saida_base = self.parameterAsFileOutput(parameters, self.SAIDA, context)
        saida_dir = os.path.dirname(saida_base)

        if not os.path.isdir(pasta_raiz):
            raise QgsProcessingException(f"A pasta especificada não existe: {pasta_raiz}")

        # Armazena para uso no postProcessAlgorithm
        self._pasta_raiz = pasta_raiz
        self._saida_dir = saida_dir
        self._camadas_criadas = []  # lista de (saida_gpkg, nome_camada, caminho_relativo_da_pasta)

        self._processarPastas(pasta_raiz, pasta_raiz, saida_dir, feedback)

        return {'OUTPUT': saida_base}

    def postProcessAlgorithm(self, context, feedback):
        """
        Monta a árvore de grupos e camadas no projeto QGIS.
        Este método roda no thread principal, com acesso seguro ao projeto.
        """
        if not self._camadas_criadas:
            feedback.pushWarning("Nenhuma imagem com GPS encontrada.")
            return {}

        root = QgsProject.instance().layerTreeRoot()
        nome_grupo_raiz = os.path.basename(self._pasta_raiz)

        # Remove grupo anterior de mesmo nome para evitar duplicatas
        grupo_existente = root.findGroup(nome_grupo_raiz)
        if grupo_existente:
            root.removeChildNode(grupo_existente)

        grupo_raiz = root.insertGroup(0, nome_grupo_raiz)

        for saida_gpkg, nome_camada, rel_pasta in self._camadas_criadas:
            feedback.pushInfo(f"Carregando camada: {nome_camada} ({saida_gpkg})")

            camada = QgsVectorLayer(saida_gpkg, nome_camada, "ogr")
            if not camada.isValid():
                feedback.pushWarning(f"Camada inválida: {saida_gpkg}")
                continue

            # Adiciona ao projeto sem inserir na raiz
            QgsProject.instance().addMapLayer(camada, False)

            # Navega/cria grupos conforme o caminho relativo da pasta
            # rel_pasta ex: "subpasta1/subpasta2"  ou  "." para raiz
            partes = [] if rel_pasta == '.' else rel_pasta.split(os.sep)

            grupo_atual = grupo_raiz
            for parte in partes:
                filho = grupo_atual.findGroup(parte)
                if filho is None:
                    filho = grupo_atual.addGroup(parte)
                grupo_atual = filho

            grupo_atual.addLayer(camada)

        return {}

    # Percorre pastas e gera os GPKGs 

    def _processarPastas(self, pasta_atual, pasta_raiz, saida_dir, feedback):
        imagens = self._loadImagesDataset(pasta_atual)

        if imagens:
            rel_pasta = os.path.relpath(pasta_atual, pasta_raiz)
            nome_camada = os.path.basename(pasta_atual)

            # Nome único para o arquivo gpkg baseado no caminho relativo
            nome_arquivo = rel_pasta.replace(os.sep, '__') + '.gpkg'
            saida_gpkg = os.path.join(saida_dir, nome_arquivo)

            feedback.pushInfo(f"Gerando GeoPackage: {saida_gpkg}")
            self._createGeometry(imagens, saida_gpkg, feedback)

            self._camadas_criadas.append((saida_gpkg, nome_camada, rel_pasta))

        subpastas = sorted([
            d for d in os.listdir(pasta_atual)
            if os.path.isdir(os.path.join(pasta_atual, d))
        ])

        for subpasta in subpastas:
            caminho_sub = os.path.join(pasta_atual, subpasta)
            if self._hasImagesRecursive(caminho_sub):
                self._processarPastas(caminho_sub, pasta_raiz, saida_dir, feedback)

    def _hasImagesRecursive(self, pasta):
        for root_dir, dirs, files in os.walk(pasta):
            for f in files:
                if self._check_image_extension(f):
                    exif = self._getExif(os.path.join(root_dir, f))
                    lon, lat, ele = self._getCoordinates(exif.get('GPSInfo', {}))
                    if lon is not None:
                        return True
        return False

    def _loadImagesDataset(self, imagesFolderPath):
        dataset = []
        try:
            entries = os.listdir(imagesFolderPath)
        except PermissionError:
            return dataset

        for filename in entries:
            filepath = os.path.join(imagesFolderPath, filename)
            if not os.path.isfile(filepath):
                continue
            if not self._check_image_extension(filename):
                continue
            exif = self._getExif(filepath)
            lon, lat, ele = self._getCoordinates(exif.get('GPSInfo', {}))
            if lon is not None and lat is not None and ele is not None:
                dataset.append((filename, lon, lat, ele))
        return dataset

    def _check_image_extension(self, filename):
        return bool(re.search(r"\.(jpg)$", filename, re.IGNORECASE))

    def _getExif(self, filename):
        try:
            raw = Image.open(filename)._getexif()
            info = {}
            if raw is not None:
                for key, value in raw.items():
                    name = TAGS.get(key, key)
                    info[name] = value
                if 'GPSInfo' in info:
                    gps_info = {}
                    for k, v in info['GPSInfo'].items():
                        gps_info[GPSTAGS.get(k, k)] = v
                    info['GPSInfo'] = gps_info
            return info
        except Exception:
            return {}

    def _getCoordinates(self, info):
        try:
            for key in ['Latitude', 'Longitude', 'Altitude']:
                if key == 'Altitude' and f'GPS{key}' in info:
                    info[key] = float(info[f'GPS{key}'])
                elif f'GPS{key}' in info and f'GPS{key}Ref' in info:
                    deg, minutes, seconds = info[f'GPS{key}']
                    direction = info[f'GPS{key}Ref']
                    info[key] = self._gms2degrees(deg, minutes, seconds, direction)
            return info.get('Longitude'), info.get('Latitude'), info.get('Altitude')
        except Exception:
            return None, None, None

    def _gms2degrees(self, deg, minutes, seconds, direction):
        return (float(deg) + float(minutes) / 60 + float(seconds) / 3600) * (
            -1 if direction in ['W', 'S'] else 1
        )

    def _createGeometry(self, dataset, saida, feedback):
        qgs_fields = QgsFields()
        for field in [
            QgsField("filename", QVariant.String),
            QgsField("lon",      QVariant.Double),
            QgsField("lat",      QVariant.Double),
            QgsField("ele",      QVariant.Double),
        ]:
            qgs_fields.append(field)

        writer = QgsVectorFileWriter(
            saida, 'UTF-8', qgs_fields,
            QgsWkbTypes.Point,
            QgsCoordinateReferenceSystem("EPSG:4326"),
            "GPKG"
        )

        if writer.hasError() != QgsVectorFileWriter.NoError:
            raise QgsProcessingException(f"Erro ao criar GeoPackage: {writer.errorMessage()}")

        for filename, lon, lat, ele in dataset:
            feat = QgsFeature()
            feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(lon, lat)))
            feat.setAttributes([filename, lon, lat, ele])
            writer.addFeature(feat)

        del writer

    # ------------------------------------------------------------------
    # Metadados do algoritmo
    # ------------------------------------------------------------------

    def name(self):
        return 'image2geom'

    def displayName(self):
        return '1. Exibir posição das imagens'

    def group(self):
        return 'Pré-processamento'

    def groupId(self):
        return 'pre_processamento'

    def createInstance(self):
        return ImageToGeometry()