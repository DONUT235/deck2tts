import os
import urllib.request
import scryfall

class ImageOpener:
    def getImage(self, card):
        #todo get image data
        pass

class ImageDownloader:
    def __init__(self, cache_name, datasource):
        self.cache_name = cache_name
        self.datasource = datasource
        self.opener = ImageOpener()
        try:
            os.mkdir(cache_name)
        except FileExistsError:
            #image cache already exists
            pass

    def getImage(self, card):
        filename = card.name
        if card.set is not None:
            filename = card.set+'-'+filename
        if card.isAlternateSide():
            filename = filename+'-'+card.face
        try:
            open(self.cache_name+os.pathsep+filename)
        except FileNotFoundError:
            self._download(card.image)
        self.opener.getImage(self, card)
        pass
    
    def _download(self, url):
        #TODO download image
        pass

if __name__ == '__main__':
    cache = ImageLocator('card-images')
    datasource = scryfall.ScryfallDataSource()
