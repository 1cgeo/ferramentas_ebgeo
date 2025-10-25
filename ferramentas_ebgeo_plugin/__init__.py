from .main import Main
from qgis.core import QgsApplication
from .provider import FerramentasebgeoProvider

def classFactory(iface):
    return Main(iface)

def registerProcessingProvider():
    global ferramentasebgeo_provider
    ferramentasebgeo_provider = FerramentasebgeoProvider()
    QgsApplication.processingRegistry().addProvider(ferramentasebgeo_provider)

def unloadProcessingProvider():
    global ferramentasebgeo_provider
    if ferramentasebgeo_provider is not None:
        QgsApplication.processingRegistry().removeProvider(ferramentasebgeo_provider)
        ferramentasebgeo_provider = None