from abc import ABC, abstractmethod
from enum import Enum
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os

def gms2degrees(deg, minutes, seconds, direction):
    return (float(deg) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if direction in ['W', 'S'] else 1)

class CameraImage(ABC):
    REQUIRED_KEYS = []

    def __init__(self, imagePath):
        self.imagePath = imagePath
        self.metadata = self.loadMetadata()
        self.validateMetadata()

    @staticmethod
    def readMetadataOnly(imagePath):
        with Image.open(imagePath) as img:
            exif = img._getexif()

        if exif is None:
            return {}

        metadata = {}
        for key, value in exif.items():
            name = TAGS.get(key, key)
            metadata[name] = value

        if 'GPSInfo' in metadata:
            gps_info = {}
            for key in metadata['GPSInfo']:
                name = GPSTAGS.get(key, key)
                gps_info[name] = metadata['GPSInfo'][key]
            metadata['GPSInfo'] = gps_info

        if 'GPSInfo' in metadata:
            gps = metadata['GPSInfo']
            for key in ['Latitude', 'Longitude', 'Altitude']:
                if key == 'Altitude' and 'GPS' + key in gps:
                    gps[key] = float(gps['GPS' + key])
                elif 'GPS' + key in gps and 'GPS' + key + 'Ref' in gps:
                    deg, minutes, seconds = gps['GPS' + key]
                    direction = gps['GPS' + key + 'Ref']
                    gps[key] = gms2degrees(deg, minutes, seconds, direction)
            if all(k in gps for k in ['Latitude', 'Longitude', 'Altitude']):
                metadata['longLatAlt'] = [gps['Longitude'], gps['Latitude'], gps['Altitude']]

        return metadata

    def loadMetadata(self):
        metadata = self.readMetadataOnly(self.imagePath)
        if not metadata:
            return {}
        return metadata
    
    def validateMetadata(self):
        missing = [k for k in self.REQUIRED_KEYS if k not in self.metadata]
        if missing:
            raise ValueError(f"Metadados com chaves obrigatórias ausentes: {missing}")

    def getLongLatAlt(self):
        return self.metadata['longLatAlt']
    
    def getImageName(self):
        return os.path.basename(self.imagePath).split('.')[0]

    @staticmethod
    @abstractmethod
    def can_handle(metadata) -> bool:
        pass
    
    @abstractmethod
    def getImageNumber(self):
        pass
    
    @abstractmethod
    def getImageRange(self):
        pass
    
    @abstractmethod
    def getYearMonthDay(self):
        pass
    
    @abstractmethod
    def getHourMinuteSecond(self):
        pass

    @abstractmethod
    def getMeshRotationY(self):
        pass

class GoProFusionImage(CameraImage):
    REQUIRED_KEYS = ['Make', 'GPSInfo']
    MESH_ROTATION_Y = 20

    @staticmethod
    def can_handle(metadata):
        isMakeGoPro = 'Make' in metadata and metadata['Make'] == 'GoPro'
        gps = metadata.get('GPSInfo', {})
        hasKeyMetadata = 'GPSTimeStamp' in gps and 'GPSDateStamp' in gps
        return isMakeGoPro and hasKeyMetadata

    def getYearMonthDay(self):
        return self.metadata['GPSInfo']['GPSDateStamp'].split(':')
    
    def getHourMinuteSecond(self):
        return self.metadata['GPSInfo']['GPSTimeStamp']
    
    def getImageNumber(self):
        return int(os.path.basename(self.imagePath).split('.')[0].split('_')[-1])
    
    def getImageRange(self):
        return int(os.path.basename(self.imagePath).split('.')[0].split('_')[-2])
    
    def getMeshRotationY(self):
        return self.MESH_ROTATION_Y
    
class Insta360Pro2Image(CameraImage):
    REQUIRED_KEYS = ['Make', 'DateTime']
    MESH_ROTATION_Y = 60

    @staticmethod
    def can_handle(metadata):
        isMakeInsta360 = 'Make' in metadata and metadata['Make'] == 'Insta360'
        hasKeyMetadata = 'DateTime' in metadata
        return isMakeInsta360 and hasKeyMetadata
    
    def getYearMonthDay(self):
        return self.metadata['DateTime'].split(' ')[0].split(':')
    
    def getHourMinuteSecond(self):
        return self.metadata['DateTime'].split(' ')[1].split(':')
    
    def getImageNumber(self):
        return int(os.path.basename(self.imagePath).split('.')[0].split('_')[-1])
    
    def getImageRange(self):
        return int(os.path.basename(self.imagePath).split('.')[0].split('_')[2])
    
    def getMeshRotationY(self):
        return self.MESH_ROTATION_Y
    
class CameraFactory:
    CAMERA_CLASSES = [GoProFusionImage, Insta360Pro2Image]

    @classmethod
    def from_image(cls, imagePath):
        metadata = CameraImage.readMetadataOnly(imagePath)
        for cam_class in cls.CAMERA_CLASSES:
            if not cam_class.can_handle(metadata):
                continue
            return cam_class(imagePath)

        # raise ValueError(f"Tipo de câmera desconhecido ou não suportado para a imagem: {imagePath}")
        print(f"Tipo de câmera desconhecido ou não suportado para a imagem: {imagePath}")

class CameraType(Enum):
    GOPROFUSION = GoProFusionImage
    INSTA360PRO2 = Insta360Pro2Image