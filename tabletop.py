from abc import ABC, abstractmethod
from sheet import TTSCardSheetManager
import json

def DEFAULT_TRANSFORM(): 
    return {
        'posX': 0,
        'posY': 1,
        'posZ': 0,
        'rotX': 0,
        'rotY': 180,
        'rotZ': 180,
        'scaleX': 1,
        'scaleY': 1,
        'scaleZ': 1,
    }

class EmptyDeckError(Exception):
    pass

class TTSDeckObject:
    def __init__(self, deck_name, upload=True):
        self.sheet_manager = TTSCardSheetManager(deck_name, upload)
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

    def _add_deck(self, deck, object_list, posX=0, log=False, name=''):
        try:
            deck_data = deck.toTTS(posX, log=log, name=name)
            object_list.append(deck_data)
            #slide the deck to the left each time the method is called
            return posX-4
        except EmptyDeckError:
            return posX

    def to_json(self, log=False):
        object_list = []
        posX = self._add_deck(
            self.main, object_list, log=log, name='main deck')
        posX = self._add_deck(
            self.command_zone, object_list, posX=posX, log=log, name='commander')
        posX = self._add_deck(
            self.extra, object_list, posX=posX, log=log, name='token deck')
        posX = self._add_deck(
            self.side, object_list, posX=posX, log=log, name='side deck')
        tts_data = {'ObjectStates': object_list}
        return json.dumps(tts_data)

class TTSDeckBase(ABC):
    @abstractmethod
    def __init__(self, sheet_manager):
        self.cards = None
        self.sheet_manager = sheet_manager

    @abstractmethod
    def get_count(self, card):
        pass

    def toTTS(self, posX, log=False, name=''):
        deck_size = sum(self.get_count(card) for card in self)
        if deck_size == 0:
            raise EmptyDeckError()
        elif deck_size == 1:
            tts_data = {'Name': 'Card'}
        else:
            tts_data = {'Name': 'DeckCustom'}
        tts_data['Transform'] = DEFAULT_TRANSFORM()
        tts_data['Transform']['posX'] = posX
        current_id = 0
        #CustomDeck dict of card sheets
        tts_data['CustomDeck'] = {}

        if tts_data['Name'] == 'DeckCustom':
            #ContainedObjects list of Cards
            tts_data['ContainedObjects'] = []
            #DeckIDs list of IDs
            tts_data['DeckIDs'] = []
            for card in self:
                count = self.get_count(card)
                if log:
                    print('Converting:', card.name)
                card_id = self.sheet_manager.add_card(card.open_image(), id(self))
                for _ in range(count):
                    tts_data['DeckIDs'].append(card_id)
                    tts_data['ContainedObjects'].append(card.toTTS(card_id))
        else:
            only_card = list(self)[0]
            if log:
                print('Converting:', only_card.name)
            tts_data['Nickname'] = only_card.name
            tts_data['CardID'] = self.sheet_manager.add_card(
                only_card.open_image(), id(self))
        for deck_number, sheet in self.sheet_manager.get_sheets(id(self)):
            if log:
                print("Generating", name, "image.")
            tts_data['CustomDeck'][deck_number] = (
                self.sheet_manager.sheet_to_TTS(deck_number))
        return tts_data


class TTSSingleDeck(TTSDeckBase):
    def __init__(self, sheet_manager):
        super().__init__(sheet_manager)
        self.cards = {}

    def __iter__(self):
        return iter(self.cards.keys())

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

    def __iter__(self):
        return iter(self.cards)

    def add_card(self, card):
        self.cards.add(card)

    def get_count(self, card):
        if card in self.cards:
            return 1
        else:
            return 0
