import images
from scryfall import ScryfallCardFactory
from abc import ABC, abstractmethod
import os
import os.path
#How will we store the deck during conversion? Maybe dict: Card->Count?

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
    def openImage(self):
        pass

    def __hash__(self):
        return hash((self.name, self.image))

_cache_name = 'card-images'
try:
    os.mkdir(_cache_name)
except FileExistsError:
    #image cache already exists
    pass

def cache_location(filename):
    return os.path.join(_cache_name, filename)

class OnlineTTSCard(TTSCardBase):
    def __init__(self, name, image, mtg_set='', face=0):
        super().__init__(name, image)
        self.set = mtg_set
        self.face = face

    def openImage(self):
        filename = self._filename()
        if not os.path.exists(filename):
            images.download(self.image, filename)
        return images.openImage(filename)

    def _filename(self):
        filename = self.name
        if self.set is not None:
            filename = self.set+'-'+filename
        if self.face != 0:
            filename = filename+'-'+str(self.face)
        extension = self.image.split('.')[-1]
        return cache_location(filename+'.'+extension)

class CustomTTSCard(TTSCardBase):
    def __init__(self, name, image):
        super(self).__init__(name, image)
        self.image_opener = downloads.ImageOpener()

    def openImage(self):
        images.openImage(self.image)


class TTSDeck:
    def __init__(self):
        self.main = {}
        self.side = set()

    def add_main(card, count):
        if new_card in self.main:
            self.main[new_card] += count
        else:
            self.main[new_card] = count

    def _add_side(card):
        side.add(card)
