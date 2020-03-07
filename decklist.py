from abc import ABC, abstractmethod
import cards
from tabletop import TTSDeck
import re

class DecklistReader(ABC):
    def __init__(self, datasource, addRelated=True):
        self.datasource = datasource
        self.addRelated = addRelated
        self.deck = TTSDeck()
        self.state = 'Main'
        self._setup_stragegies()

    @abstractmethod
    def _setup_stragegies(self):
        pass

    def read_list(self, filename):
        decklist = open(filename)
        for line in decklist:
            self.processCard(line)
        return self.deck

    def processCard(self, line):
        next_state = self.line_decision_strategy(line)
        if next_state != 'Card':
            if next_state != 'Same':
                self.state = next_state
            return

        if self.state == 'Maybeboard':
            return

        is_sideboard, name, count, mtg_set, comment = self.card_reader_strategy(line)
        newcard = None
        if '!Custom' in comment:
            filename_pattern = r'!Custom\(([^)]+)\)'
            filename_match = re.search(filename_pattern, line)
            image = filename_match.group(1)
            newcard = cards.CustomTTSCard(name, image)
        else:
            newcard = self.datasource.make_card(name, mtg_set)
            associated_cards = self.datasource.make_related(name, mtg_set)
            for associated_card in associated_cards:
                self.deck.add_extra(associated_card)

        if '!Commander' in comment:
            self.deck.add_commander(newcard)
            return

        if self.state == 'Side':
            self.deck.add_side(newcard, count)
        else:
            self.deck.add_main(newcard, count)


_deckstats_card_pattern = re.compile(
    r'(?P<sideboard>SB: )?(?P<count>\d+) (\[(?P<set>[^]]+)\] )?'
    + r'(?P<name>[^#]+)(?P<comment>#.*)?')

def _deckstats_line_decision(line):
    if line in ('Sideboard', '//Sideboard'):
        return 'Side'

    if line == '//Maybeboard':
        return 'Maybeboard'

    match = _deckstats_card_pattern.match(line)
    if match is None:
        if line[0:2] != '//':
            print('Bad formatting: Line',line,'will be ignored.')
            return 'Same'
        else:
            #found a custom category
            return 'Main'

    return 'Card'

def _deckstats_card_reader(line):
    match = _deckstats_card_pattern.match(line)
    sideboard, name, count, mtg_set, comment = map(
        lambda s: (s.strip() if s is not None else ''),
        match.group('sideboard', 'name', 'count', 'set', 'comment'))
    sideboard = bool(sideboard)
    count = int(count)
    return (sideboard, name, count, mtg_set, comment)


class DeckstatsDecklistReader(DecklistReader):
    def _setup_stragegies(self):
        self.line_decision_strategy = _deckstats_line_decision
        self.card_reader_strategy = _deckstats_card_reader

def _blank_line_decision(line):
    if line.strip() == '':
        return 'Side'
    else:
        return 'Card'

_mtgo_card_pattern = re.compile(
    r'(?P<count>\d+) (?P<name>.+) \((?P<set>[^)]+)\) \d+')
def _mtgo_card_reader(line):
    match = _mtgo_card_pattern.match(line)
    count, name, mtg_set = map(
        str.strip, match.group('count', 'name', 'set'))
    count = int(count)
    return (False, name, count, mtg_set, '')

class MTGODecklistReader(DecklistReader):
    def _setup_stragegies(self):
        self.line_decision_strategy = _blank_line_decision
        self.card_reader_strategy = _mtgo_card_reader
