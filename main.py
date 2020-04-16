import argparse
import sys
from decklist.deckstats import DeckstatsDecklistReader
from decklist.mtgo import MTGODecklistReader
from decklist.arena import ArenaDecklistReader
import scryfall
import imgur
from images import cache_location

DEFAULT_IMAGE = cache_location('default.jpg')

def main():
    parser = argparse.ArgumentParser(
        description='Tabletop Simulator Deck Generator')
    parser.add_argument(
        '-f', '--format',
        choices=(
            'MTGO', 'mtgo',
            'Arena', 'arena',
            'Deckstats', 'deckstats'),
        default='deckstats',
        help='Format for the decklist file')
    parser.add_argument(
        '-n', '--no_upload', default=False, const=True, action='store_const',
        help='if specified, do not upload the file to imgur')
    parser.add_argument(
        'decklist_file',
        help='Name of the text file containing the decklist')
    parser.add_argument(
        'deck_name',
        help='Name of the Tabletop Simulator saved object to be created')
    arguments = parser.parse_args()
    decklist_format = arguments.format.lower()
    name = arguments.deck_name
    datasource = scryfall.ScryfallCardFactory(DEFAULT_IMAGE)
    upload = not arguments.no_upload
    if upload:
        imgur.authorize()
    if decklist_format == 'arena':
        reader = ArenaDecklistReader(name, datasource, upload=upload, log=True)
    elif decklist_format == 'mtgo':
        reader = MTGODecklistReader(name, datasource, upload=upload, log=True)
    else:
        reader = DeckstatsDecklistReader(
            name, datasource, upload=upload, log=True)
    for line in open(arguments.decklist_file):
        print('Reading line:', line.strip())
        reader.processCard(line)
    tts_json = reader.deck.to_json()
    out = open(name+'.json','w')
    out.write(tts_json)

if __name__ == '__main__':
    main()
