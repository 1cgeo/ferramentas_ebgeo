"""
/***************************************************************************
 Listar Imagens
                                 A QGIS plugin
 Conjunto de ferramentas do Streetview do 1° CGEO.
                              -------------------
        begin                : 2024-11-26
        copyright            : (C) 2024 by Brazilian Army Cartographic
        email                : raulmagno.neves@eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   Este programa é um software livre; você pode redistribuí-lo e/ou     *
 *   modificá-lo sob os termos da Licença Pública Geral GNU conforme      *
 *   publicada pela Free Software Foundation; versão 2 ou posterior.      *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = '1° Ten Raul Magno / 1° CGEO'
__date__ = '2025-04-17'
__copyright__ = '(C) 2024 by Brazilian Army Cartographic Mapoteca Tools'

from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsProcessingAlgorithm,
    QgsVectorLayer,
    QgsField,
    QgsFields,
    QgsFeature,
    QgsProject,
    QgsProcessingException,
    QgsVectorFileWriter,
    QgsWkbTypes,
    QgsCoordinateReferenceSystem
)
from PyQt5.QtCore import QVariant
import os
import re


class ListImages(QgsProcessingAlgorithm):

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
                'Arquivo de saída (GeoPackage)',
                fileFilter='GeoPackage (*.gpkg)'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        pasta = self.parameterAsFile(parameters, self.PASTA, context)
        saida = self.parameterAsFileOutput(parameters, self.SAIDA, context)

        if not os.path.isdir(pasta):
            raise QgsProcessingException(
                f"A pasta especificada não existe: {pasta}"
            )

        dataset = self.loadImagesList(pasta, feedback)
        self.createPointLayer(dataset, saida, context, feedback)

        return {'OUTPUT': saida}

    def loadImagesList(self, imagesFolderPath, feedback):
        dataset = []
        image_count = 0

        for filename in os.listdir(imagesFolderPath):
            if not self.check_image_extension(filename):
                continue

            image_count += 1
            full_path = os.path.join(imagesFolderPath, filename)
            file_size = os.path.getsize(full_path)
            
            # Extrair nome sem extensão
            nome_sem_extensao = os.path.splitext(filename)[0]

            dataset.append((filename, nome_sem_extensao, full_path, file_size))

        feedback.pushInfo(f"Total de imagens encontradas: {image_count}")
        return dataset

    def check_image_extension(self, filename):
        return bool(
            re.search(r"\.(jpg|jpeg|png|gif|bmp|tiff|json)$", filename, re.IGNORECASE)
        )

    def createPointLayer(self, dataset, saida, context, feedback):

        # Definição dos campos
        fields = QgsFields()
        fields.append(QgsField("filename", QVariant.String))
        fields.append(QgsField("nome_img", QVariant.String))
        fields.append(QgsField("caminho_completo", QVariant.String))
        fields.append(QgsField("tamanho_bytes", QVariant.Int))

        # Criar camada de PONTOS (mesmo sem geometria nas feições)
        writer = QgsVectorFileWriter(
            saida,
            'UTF-8',
            fields,
            QgsWkbTypes.Point,  # ← camada de pontos
            QgsCoordinateReferenceSystem("EPSG:4326"),
            "GPKG"
        )

        if writer.hasError() != QgsVectorFileWriter.NoError:
            raise QgsProcessingException(
                f"Erro ao criar o GeoPackage: {writer.errorMessage()}"
            )

        # Criar feições SEM geometria
        for filename, nome_sem_extensao, full_path, file_size in dataset:
            feat = QgsFeature(fields)
            feat.setAttributes([
                filename,
                nome_sem_extensao,
                full_path,
                file_size
            ])
            # Não definir geometria → geometria nula
            writer.addFeature(feat)

        del writer  # Finaliza a escrita

        # Carregar a camada no projeto
        camada = QgsVectorLayer(saida, "Lista_Imagens", "ogr")
        if camada.isValid():
            QgsProject.instance().addMapLayer(camada)
            feedback.pushInfo("Camada de pontos criada e carregada com sucesso!")
        else:
            feedback.pushWarning(
                "A camada foi criada, mas não pôde ser carregada automaticamente."
            )

    def name(self):
        return 'listimages'

    def displayName(self):
        return '0. Listar Imagens da Pasta'

    def group(self):
        return 'Pré-processamento'

    def groupId(self):
        return 'pre_processamento'

    def createInstance(self):
        return ListImages()