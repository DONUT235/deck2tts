import images
from abc import ABC, abstractmethod
import os
import os.path
import downloads
import json
from tabletop import DEFAULT_TRANSFORM

_cache_name = 'card-images'
try:
    os.mkdir(_cache_name)
except FileExistsError:
    #image cache already exists
    pass

def cache_location(filename):
    return os.path.join(_cache_name, filename)


class TTSCardBase(ABC):
    def __init__(self, name, image):
        self.name = name
        self.image = image

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.name == other.name and self.image == other.image:
                return True
        return False

    @abstractmethod
    def open_image(self):
        pass

    def __hash__(self):
        return hash((self.name, self.image))

    def toTTS(self, card_id):
        tts_data = {'Name': 'Card'}
        tts_data['Nickname'] = self.name
        tts_data['Transform'] = DEFAULT_TRANSFORM
        tts_data['CardID'] = card_id
        return tts_data


class OnlineTTSCard(TTSCardBase):
    def __init__(self, name, image, mtg_set='', face=0):
        super().__init__(name, image)
        self.set = mtg_set
        self.face = face

    def open_image(self):
        filename = self.filename()
        if not os.path.exists(filename):
            downloads.download(self.image, filename)
        return images.open_image(filename)

    def filename(self):
        filename = self.name
        if self.set != '':
            filename = self.set+'-'+filename
        if self.face != 0:
            filename = filename+'-'+str(self.face)
        extension = self.image.split('.')[-1]
        return cache_location(filename+'.'+extension)


class CustomTTSCard(TTSCardBase):
    def open_image(self):
        return images.open_image(self.image)
