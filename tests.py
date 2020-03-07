from scryfall import ScryfallCardFactory
import cards
import images
import unittest
import os.path
from time import sleep

class ScryfallTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ds = ScryfallCardFactory(cards.cache_location('default.jpg'))
    def test_werewolf(self):
        werewolf = self.ds.make_card('Gatstaf Arsonists // Gatstaf Ravagers')
        self.assertEqual(werewolf.name, 'Gatstaf Arsonists')
        print(werewolf.image)
        print(werewolf.filename())

    def test_forest(self):
        forest = self.ds.make_card('Forest', 'C16')
        self.assertEqual(forest.name, 'Forest')
        self.assertEqual(forest.set, 'C16')
        print(forest.image)
        print(forest.filename())

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
        image_data.close()

class PillowTests(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.back = images.openImage('card-images\\CardBack.jpg')
        cls.img_size = (488, 680)
        cls.default = images.openImage('card-images\\default.jpg')

    def test_two_card_backs(self):
        grid_size = (2, 1)
        combined = images.combine(
            [self.default, self.back], grid_size,
            self.img_size, 'combined.jpg')
        #if nothing broke the test passed.
        self.assertEqual(combined.size, (self.img_size[0]*2, self.img_size[1]))
        combined.show()

    def test_big(self):
        deck = [self.default for _ in range(69)]
        deck.append(self.back)
        grid_size = (10, 7)
        big = images.combine(
            deck, grid_size,
            self.img_size, 'big.jpg')
        expectedHeight = int(4096/(10*self.img_size[0])*7*self.img_size[1])
        self.assertEqual(big.size, (4096, expectedHeight))
        big.show()

if __name__ == '__main__':
    unittest.main()
