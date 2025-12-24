from qgis.core import QgsProcessingProvider
from .processings.recuperar.Converte_para_JPG import ConverterParaJPEG  # Comprime imagens JPEG
from .processings.compactar.compactar import ComprimirImagensExifTool  # Plota pontos das imagens
from .processings.pre_processar.Listar_imagens import ListImages  # Plota pontos das imagens
from .processings.pre_processar.Pontos_imagens import ImageToGeometry  # Plota pontos das imagens
from .processings.pre_processar.Remove_pontos_parada import RemovePontosDeParada  # Copia imagens
from .processings.pre_processar.Copia_imagens import CopiaImagens  # Copia imagens
from .processings.recuperar.Adiciona_coordenadas_EXIF import AdicionaCoordenadasExiftool  # Adiciona metadados GPS
from .processings.vetores_ebgeo.construir_estilo import ConstruiEstilo
from .processings.vetores_ebgeo.gerarGeoJSON import ExportPostGISGeoJSONAlgorithm
from .processings.vetores_ebgeo.construir_grid import ExportGridAlgorithm
from .processings.recuperar.Recupera_coordenadas import RecuperarCoordenadasMetadado  # Adiciona metadados GPS
from .processings.recuperar.Adiciona_coordenadas_EXIF_GPSDate import AdicionaCoordenadasExiftoolGPSDate  # Adiciona metadados GPS com data
from .processings.recuperar.Recupera_coordenadas_GPSDate import RecuperarCoordenadasMetadadoGPSDate  # Adiciona metadados GPS
from qgis.PyQt.QtGui import QIcon
import os

class FerramentasebgeoProvider(QgsProcessingProvider):
    def loadAlgorithms(self):
        self.addAlgorithm(ConverterParaJPEG())
        self.addAlgorithm(ComprimirImagensExifTool())
        self.addAlgorithm(ListImages())
        self.addAlgorithm(ImageToGeometry())
        self.addAlgorithm(RemovePontosDeParada())
        self.addAlgorithm(CopiaImagens())
        self.addAlgorithm(AdicionaCoordenadasExiftool())
        self.addAlgorithm(ConstruiEstilo())
        self.addAlgorithm(ExportPostGISGeoJSONAlgorithm())
        self.addAlgorithm(ExportGridAlgorithm())
        self.addAlgorithm(RecuperarCoordenadasMetadado())
        self.addAlgorithm(RecuperarCoordenadasMetadadoGPSDate())
        self.addAlgorithm(AdicionaCoordenadasExiftoolGPSDate())

    def id(self):
        return "ferramentasebgeo"

    def name(self):
        return "Ferramentas EBGeo"

    def longName(self):
        return self.name()

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), 'icons', 'logo_ebgeo.png'))
