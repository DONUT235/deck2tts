from abc import ABC, abstractmethod
import cards
from tabletop import TTSDeckObject
import re

class DecklistReader(ABC):
    def __init__(self, deck_name, datasource,
            addRelated=True, upload=True, log=False):
        self.datasource = datasource
        self.addRelated = addRelated
        self.deck = TTSDeckObject(deck_name, upload=upload, log=log)
        self.state = 'Main'

    @abstractmethod
    def card_reader_strategy(self, line):
        r"""Handles lines corresponding to MTG cards.
        Returns (name, count, is_sideboard, mtg_set, comment)
        as a tuple if a card was found. Returns None in 'name'
        if no card was found."""
        return (None, 0, False, '', '')

    @abstractmethod
    def line_decision_strategy(self, line):
        r"""Handles lines that may or may not be cards.
        Returns one of the following: 
        'Card': The line is a card.
        'Same': Don't do anything with this line.
        'Side': Put subsequent cards in the sideboard.
        'Main': Put subsequent cards in the main deck.
        'Maybeboard': Ignore subsequent cards."""
        return 'Same'

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

        name, count, is_sideboard, mtg_set, comment = self.card_reader_strategy(line)
        if name is None:
            print('Bad formatting: Line',line,'will be ignored.')
            return

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

class RegexCardReaderStrategy(ABC):
    def __call__(self, line):
        match = self.pattern.match(line)
        if match is None:
            return (None, 0, False, '', '')
        name, count = map(
            str.strip, match.group('name', 'count'))
        count = int(count)
        is_sideboard, mtg_set, comment = self.other_props(match)
        return (name, count, is_sideboard, mtg_set, comment)

    @property
    @abstractmethod
    def pattern(self):
        """Compiled regex pattern. Should have 'name' and 'count' groups."""
        pass

    def other_props(self, match):
        """Return (is_sideboard, mtg_set, comment) as a tuple."""
        return (False, '', '')
