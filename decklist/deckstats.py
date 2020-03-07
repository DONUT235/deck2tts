from decklist import RegexCardReaderStrategy, DecklistReader
import re
class DeckstatsCardReader(RegexCardReaderStrategy):
    pattern = re.compile(
        r'(?P<sideboard>SB: )?(?P<count>\d+) (\[(?P<set>[^]]+)\] )?'
        + r'(?P<name>[^#]+)(?P<comment>#.*)?')

    def other_props(self, match):
        sideboard, mtg_set, comment = map(
            lambda s: (s.strip() if s is not None else ''),
            match.group('sideboard', 'set', 'comment'))
        sideboard = bool(sideboard)
        return (sideboard, mtg_set, comment)

class DeckstatsDecklistReader(DecklistReader):
    def line_decision_strategy(self, line):
        if line in ('Sideboard', '//Sideboard'):
            return 'Side'
        if line == '//Maybeboard':
            return 'Maybeboard'

        match = DeckstatsCardReader.pattern.match(line)
        if match is None:
            if line[0:2] != '//':
                return 'Card'
            else:
                #found a custom category
                return 'Main'
        return 'Card'

    card_reader_strategy = DeckstatsCardReader()
