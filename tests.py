from scryfall import ScryfallCardFactory
import cards
import images
import unittest

class ScryfallTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ds = ScryfallCardFactory(cards.cache_location('CardBack.jpg'))
    def test_werewolf(self):
        werewolf = self.ds.make_card('Gatstaf Arsonists // Gatstaf Ravagers')
        self.assertEqual(werewolf.name, 'Gatstaf Arsonists')
        print(werewolf.image)
        print(werewolf._filename())

    def test_forest(self):
        forest = self.ds.make_card('Forest', 'C16')
        self.assertEqual(forest.name, 'Forest')
        self.assertEqual(forest.set, 'C16')
        print(forest.image)
        print(forest._filename())

if __name__ == '__main__':
    unittest.main()
