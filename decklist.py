from abc import ABC, abstractmethod
import cards
from tabletop import TTSDeck
import re

_deckstats_card_pattern = re.compile(
    r'(?P<sideboard>SB: )?(?P<count>\d+) (\[(?P<set>[^]]+)\] )?'
    + r'(?P<name>[^#]+)(?P<comment>#.*)?')

def _deckstats_line_decision_strategy(line):
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

def _deckstats_card_reader_strategy(line):
    match = _deckstats_card_pattern.match(line)
    sideboard, name, count, mtg_set, comment = map(
        lambda s: (s.strip() if s is not None else ''),
        match.group('sideboard', 'name', 'count', 'set', 'comment'))
    sideboard = bool(sideboard)
    count = int(count)
    return (sideboard, name, count, mtg_set, comment)


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
        next_state = self.line_decision(line)
        if next_state != 'Same' and next_state != 'Card':
            self.state = next_state
            return
        elif next_state == 'Same':
            return

        if self.state == 'Maybeboard':
            return

        is_sideboard, name, count, mtg_set, comment = self.card_reader(line)
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


class DeckstatsDecklistReader(DecklistReader):
    def _setup_stragegies(self):
        self.line_decision = _deckstats_line_decision_strategy
        self.card_reader = _deckstats_card_reader_strategy
