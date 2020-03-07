from decklist import RegexCardReaderStrategy
from mtgo import BlankLineDeckSeparatingReader
import re

class ArenaCardReader(RegexCardReaderStrategy):
    pattern = re.compile(
        r'(?P<count>\d+) (?P<name>.+) \((?P<set>[^)]+)\) \d+')

    def other_props(self, match):
        mtg_set = match.group('set').strip()
        return (False, mtg_set, '')

class ArenaDecklistReader(BlankLineDeckSeparatingReader):
    card_reader_strategy = ArenaCardReader()
