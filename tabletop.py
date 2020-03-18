from abc import ABC, abstractmethod

DEFAULT_TRANSFORM = {
    'posX': 0,
    'posY': 0,
    'posZ': 0,
    'rotX': 0,
    'rotY': 180,
    'rotZ': 180,
    'scaleX': 1,
    'scaleY': 1,
    'scaleZ': 1,
}

#TODO write toTTS methods in each of these which return JSON-ifiable objects
class TTSCardSheetManager:
    MAX_SIZE = 69
    def __init__(self):
        #List of Images
        self.sheets = [[]]
        #Key for CustomDeck dict, also first digit of DeckIDs ids
        self.current_number = 1
        #Second two digits of DeckIDs ids
        self.current_id = 0

    def add_card(self, img):
        if len(self.sheets[self.current_number-1]) >= 69:
            self.current_number += 1
            self.current_id = 0
            self.sheets.append([])
        self.sheets[self.current_number-1].append(img)
        returned_id = self.current_number*100+self.current_id
        self.current_id += 1
        return returned_id

class TTSDeck:
    def __init__(self):
        self.sheet_manager = TTSCardSheetManager()
        self.main = TTSSingleDeck(self.sheet_manager)
        self.side = TTSSingleDeck(self.sheet_manager)
        self.extra = TTSExtraDeck(self.sheet_manager)
        self.command_zone = TTSExtraDeck(self.sheet_manager)

    def get_main_count(self, card):
        return self.main.get_count(card)

    def get_side_count(self, card):
        return self.side.get_count(card)

    def in_extra(self, card):
        return self.extra.get_count(card) == 1

    def is_commander(self, card):
        return self.command_zone.get_count(card) == 1

    def add_main(self, card, count=1):
        self.main.add_card(card, count)

    def add_side(self, card, count=1):
        self.side.add_card(card, count)

    def add_commander(self, card):
        self.command_zone.add_card(card)

    def add_extra(self, card):
        self.extra.add_card(card)

    def _add_deck(self, deck, object_list, deck_number, posX=0):
        deck_data, inc = deck.toTTS(deck_number)
        object_list.append(deck_data)
        #slide the deck to the left each time the method is called
        return (deck_number+inc, posX-4)

    def toJSON(self):
        #use deck_number as key in "CustomDeck" dict
        deck_number = 1
        object_list = []
        deck_number, posX = self._add_deck(main, object_list, deck_number)
        deck_number, posX = self._add_deck(side, object_list, deck_number, posX)
        deck_number, posX = self._add_deck(extra, object_list, deck_number, posX)
        deck_number, posX = self._add_deck(command_zone, object_list, deck_number, posX)
        tts_json = {'ObjectStates': object_list}

class TTSDeckBase(ABC):
    @abstractmethod
    def __init__(self, sheet_manager):
        self.cards = None
        self.sheet_manager = sheet_manager

    @abstractmethod
    def get_count(self, card):
        pass
    
    def toTTS(self, deck_number, posX):
        if len(self.cards) == 0:
            return ([], 0)
        current_id = 0
        num_sheets = 0
        tts_data = {'Name': 'DeckCustom'}
        tts_data['Transform'] = DEFAULT_TRANSFORM
        tts_data['Transform']['posX'] = posX
        #TODO ContainedObjects list of Cards
        #TODO DeckIDs list of IDs
        #TODO CustomDeck dict of card sheets
        for card in self.cards:
            count = self.get_count(card)
            card_id = self.sheet_manager.add_card(card.open_image())

class TTSSingleDeck(TTSDeckBase):
    def __init__(self, sheet_manager):
        super().__init__(sheet_manager)
        self.cards = {}

    def add_card(self, card, count):
        if card in self.cards:
            self.cards[card] += count
        else:
            self.cards[card] = count

    def get_count(self, card):
        if card in self.cards:
            return self.cards[card]
        else:
            return 0

class TTSExtraDeck(TTSDeckBase):
    def __init__(self, sheet_manager):
        super().__init__(sheet_manager)
        self.cards = set()

    def add_card(self, card):
        self.cards.add(card)

    def get_count(self, card):
        if card in self.cards:
            return 1
        else:
            return 0
