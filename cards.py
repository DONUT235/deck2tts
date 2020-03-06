from images import ImageDownloader
#How will we store the deck during conversion? Maybe dict: Card->Count?
class TTSCard:
    def __init__(self, name, image, mtg_set='', face=0):
        self.name = name
        self.image = image
        self.set = mtg_set
        self.face = face
        self.image_opener = ImageDownloader()

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.name == other.name and self.image == other.image:
                return True
        return False

    def openImage():
        self.image_opener.getImage(self)

    def __hash__(self):
        return hash((self.name, self.image))

class CustomTTSCard(TTSCard):
    def __init__(self, name, image):
        super(self).__init__(name, image)
        self.image_opener = ImageOpener()


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
