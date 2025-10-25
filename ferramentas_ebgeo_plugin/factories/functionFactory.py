
from ferramentas_ebgeo_plugin.models.trackGyroscope import TrackGyroscope
from ferramentas_ebgeo_plugin.models.storageConfig import StorageConfig
from ferramentas_ebgeo_plugin.models.alarm import Alarm
from ferramentas_ebgeo_plugin.models.timer import Timer
from ferramentas_ebgeo_plugin.models.buildStruct import BuildStruct
from ferramentas_ebgeo_plugin.models.buildSiteMetadata import BuildSiteMetadata
from ferramentas_ebgeo_plugin.models.processPointsAndLines import ProcessPointsAndLines
from ferramentas_ebgeo_plugin.models.applyMask import ApplyMask
from ferramentas_ebgeo_plugin.models.applyBlurMask import ApplyBlurMask

class FunctionFactory:

    def create(self, functionName, *args):
        functions = {
            'BuildSiteMetadata': lambda *args: BuildSiteMetadata(*args),
            'TrackGyroscope': lambda *args: TrackGyroscope(*args),
            'StorageConfig': lambda *args: StorageConfig(*args),
            'Alarm': lambda *args: Alarm(*args),
            'Timer': lambda *args: Timer(*args),
            'BuildStruct': lambda *args: BuildStruct(*args),
            'ProcessPointsAndLines': lambda *args: ProcessPointsAndLines(*args),
            'ApplyMask': lambda *args: ApplyMask(*args),
            'ApplyBlurMask': lambda *args: ApplyBlurMask(*args),
        }
        return functions[functionName](*args) if functionName in functions else None