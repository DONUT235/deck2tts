from scryfall import ScryfallCardFactory
import cards
import images
import unittest
import decklist
import os.path
import tabletop
import downloads
from decklist.deckstats import DeckstatsDecklistReader
from decklist.mtgo import MTGODecklistReader
from decklist.arena import ArenaDecklistReader
from time import sleep

class ScryfallTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ds = ScryfallCardFactory(cards.cache_location('default.jpg'))

    def test_werewolf(self):
        werewolf = self.ds.make_card('Gatstaf Arsonists // Gatstaf Ravagers')
        self.assertEqual(werewolf.name, 'Gatstaf Arsonists')

    def test_forest(self):
        forest = self.ds.make_card('Forest', 'C16')
        self.assertEqual(forest.name, 'Forest')
        self.assertEqual(forest.set, 'C16')

    @unittest.skip("slow and requires internet connection")
    def test_download_ashling(self):
        ashling = self.ds.make_card('Ashling the Pilgrim')
        if os.path.exists(ashling.filename()):
            os.remove(ashling.filename())
        image_data = ashling.openImage()
        image_data.close()
        self.assertTrue(os.path.exists(ashling.filename()))
        last_modified = os.stat(ashling.filename()).st_mtime
        sleep(2)
        image_data = ashling.openImage()
        self.assertEqual(last_modified, os.stat(ashling.filename()).st_mtime)
        self.assertEqual(image_data.size, (488, 680))
        self.assertFalse(ashling.image in downloads._cache)
        image_data.close()

    def test_associated(self):
        werewolf_name = 'Gatstaf Arsonists // Gatstaf Ravagers'
        werewolf_backs = self.ds.make_related(werewolf_name)
        werewolf_backs = list(werewolf_backs)
        self.assertEqual(len(werewolf_backs), 1)
        self.assertEqual(werewolf_backs[0].name, 'Gatstaf Ravagers')

class PillowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.back = images.openImage('card-images\\CardBack.jpg')
        cls.img_size = (488, 680)
        cls.default = images.openImage('card-images\\default.jpg')

    @classmethod
    def tearDownClass(cls):
        cls.back.close()
        cls.default.close()

    def test_two_card_backs(self):
        grid_size = (2, 1)
        combined = images.combine(
            [self.default, self.back], grid_size,
            self.img_size, 'combined.jpg')
        #if nothing broke the test passed.
        self.assertEqual(combined.size, (self.img_size[0]*2, self.img_size[1]))

    def test_big(self):
        deck = [self.default for _ in range(69)]
        deck.append(self.back)
        grid_size = (10, 7)
        big = images.combine(
            deck, grid_size,
            self.img_size, 'big.jpg')
        expectedHeight = int(4096/(10*self.img_size[0])*7*self.img_size[1])
        self.assertEqual(big.size, (4096, expectedHeight))

    def test_custom_image(self):
        aaron = cards.CustomTTSCard(
            'Aaron Glave, Time Wizard', 'card-images\\aaron.jpg')
        img = aaron.openImage()
        self.assertEqual(img.size, (488, 680))
        img.close()

class TTSDeckTests(unittest.TestCase):
    def setUp(self):
        self.deck = tabletop.TTSDeck()

    def test_add_twice(self):
        card = cards.CustomTTSCard(
            'Aaron Glave, Time Wizard', 'card-images\\aaron.jpg')
        self.deck.add_main(card, 1)
        self.deck.add_main(card, 3)
        self.assertEqual(self.deck.get_main_count(card), 4)

class DecklistTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ds = ScryfallCardFactory(cards.cache_location('default.jpg'))
    def setUp(self):
        self.reader = None

    def test_bad_input(self):
        if self.reader is not None:
            self.reader.processCard('*@&&$*(@(*& Cunk Cunk #Cu#nk#')

class DeckstatsTests(DecklistTest):
    def setUp(self):
        self.reader = DeckstatsDecklistReader(self.ds)
        self.aaron = cards.CustomTTSCard(
            'Aaron Glave, Time Wizard', 'card-images\\aaron.jpg')
        self.aaron_line = '1 Aaron Glave, Time Wizard #!Custom(card-images\\aaron.jpg)'

    def test_add_with_set(self):
        self.reader.processCard('1 [C16] Forest')
        card = self.ds.make_card('Forest', 'C16')
        self.assertEqual(self.reader.deck.get_main_count(card), 1)
        for card in self.reader.deck.main.cards:
            self.assertEqual(card.set, 'C16')

    def test_add_with_count(self):
        self.reader.processCard('99 Mountain')
        card = self.ds.make_card('Mountain')
        self.assertEqual(self.reader.deck.get_main_count(card), 99)

    def test_custom(self):
        self.reader.processCard(self.aaron_line)
        self.assertEqual(self.reader.deck.get_main_count(self.aaron), 1)
        for card in self.reader.deck.main.cards:
            self.assertIsInstance(card, cards.CustomTTSCard)

    def test_sideboard(self):
        self.reader.processCard('Sideboard')
        self.reader.processCard(self.aaron_line)
        self.assertEqual(self.reader.deck.get_side_count(self.aaron), 1)
        self.assertEqual(self.reader.deck.get_main_count(self.aaron), 0)

    def test_maybeboard(self):
        self.reader.processCard('//Maybeboard')
        self.reader.processCard(self.aaron_line)
        self.assertEqual(self.reader.deck.get_main_count(self.aaron), 0)
        self.assertEqual(self.reader.deck.get_side_count(self.aaron), 0)
        self.assertFalse(self.reader.deck.is_commander(self.aaron))
        self.assertFalse(self.reader.deck.in_extra(self.aaron))

    def test_maindeck(self):
        self.reader.processCard('//Maybeboard')
        self.reader.processCard(self.aaron_line)
        self.reader.processCard('//Lands')
        self.reader.processCard(self.aaron_line)
        self.assertEqual(self.reader.deck.get_main_count(self.aaron), 1)

    def test_commander(self):
        self.reader.processCard('1 Phelddagrif #!Commander')
        commander = self.ds.make_card('Phelddagrif')
        self.assertEqual(self.reader.deck.get_main_count(commander), 0)
        self.assertTrue(self.reader.deck.is_commander(commander))

    def test_commander_whitespace(self):
        self.reader.processCard('1 Phelddagrif    #    !Commander')
        commander = self.ds.make_card('Phelddagrif')
        self.assertTrue(self.reader.deck.is_commander(commander))

    def test_custom_commander(self):
        self.reader.processCard(self.aaron_line+' !Commander')
        self.assertTrue(self.reader.deck.is_commander(self.aaron))

class ArenaTests(DecklistTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.brainstorm = cls.ds.make_card('Brainstorm', 'C18')
    def setUp(self):
        self.reader = ArenaDecklistReader(self.ds)

    def testSingleCard(self):
        self.assertEqual(self.reader.deck.get_main_count(self.brainstorm), 0)
        self.reader.processCard('1 Brainstorm (C18) 82')
        self.assertEqual(self.reader.deck.get_main_count(self.brainstorm), 1)

    def testSideDeck(self):
        self.reader.processCard('1 Brainstorm (C18) 82')
        self.reader.processCard('')
        self.reader.processCard('1 Counterspell (A25) 50')
        brainstorm = self.ds.make_card('Brainstorm', 'C18')
        counterspell = self.ds.make_card('Counterspell', 'A25')
        self.assertEqual(self.reader.deck.get_side_count(brainstorm), 0)
        self.assertEqual(self.reader.deck.get_side_count(counterspell), 1)
        self.assertEqual(self.reader.deck.get_main_count(counterspell), 0)

class MTGOTests(DecklistTest):
    def setUp(self):
        self.reader = MTGODecklistReader(self.ds)

    def testSingleCard(self):
        self.reader.processCard('2 Mountain')
        island = self.ds.make_card('Mountain')
        self.assertEqual(self.reader.deck.get_main_count(island), 2)

if __name__ == '__main__':
    unittest.main(buffer=True)
