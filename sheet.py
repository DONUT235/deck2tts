import images
import os.path
import pathlib
import imgur
CARD_BACK = 'https://i.imgur.com/DnlmYzy.jpg'

def _no_upload(image_filename):
    path = pathlib.PurePath(os.path.abspath(image_filename))
    return path.as_uri()

class TTSCardSheetManager:
    MAX_SIZE = 69
    def __init__(self, deck_name, upload=True):
        self.deck_name = deck_name
        self.flush()
        if upload:
            #TODO Upload to Imgur
            self.upload = imgur.upload
            pass
        else:
            self.upload = _no_upload

    def add_card(self, img, owner):
        if owner not in self.clients:
            self.clients[owner] = {}
        owner_sheets = self.clients[owner]
        if (self.current_number not in owner_sheets
                or len(owner_sheets[self.current_number]) >= 69):
            self.current_number += 1
            self.current_id = 0
            owner_sheets[self.current_number] = []
        current_sheet = owner_sheets[self.current_number]
        if self.current_number not in self._all_sheets:
            self._all_sheets[self.current_number] = current_sheet
        current_sheet.append(img)
        returned_id = self.current_number*100+self.current_id
        self.current_id += 1
        return returned_id

    def get_sheets(self, owner):
        yield from self.clients[owner].items()

    def flush(self):
        #List of Images
        #Key for CustomDeck dict, also first digit of DeckIDs ids
        self.current_number = 0
        #Second two digits of DeckIDs ids
        self.current_id = 0
        self.clients = {}
        self._all_sheets = {}

    def sheet_to_TTS(self, deck_number):
        sheet = self._all_sheets[deck_number]
        num_slots = len(sheet)
        height = num_slots // 10
        if num_slots % 10 != 0:
            height += 1
        if(height == 1):
            width = num_slots
        else:
            width = 10
        image_filename = '{}-{}.jpg'.format(self.deck_name,deck_number)
        images.combine(sheet, (width, height), sheet[0].size, image_filename)
        image_url = self.upload(image_filename)
        tts_data = {
            'NumWidth': width,
            'NumHeight': height,
            'BackURL': CARD_BACK,
            'FaceURL': image_url,
            'BackIsHidden': True
        }
        return tts_data
