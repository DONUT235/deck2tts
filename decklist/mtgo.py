from decklist import DecklistReader, RegexCardReaderStrategy
import re
class BlankLineDeckSeparatingReader(DecklistReader):
    def line_decision_strategy(self, line):
        if line.strip() == '':
            return 'Side'
        else:
            return 'Card'

class MTGOCardReader(RegexCardReaderStrategy):
    pattern = re.compile(r'(?P<count>\d+) (?P<name>.+)')

class MTGODecklistReader(BlankLineDeckSeparatingReader):
    card_reader_strategy = MTGOCardReader()
