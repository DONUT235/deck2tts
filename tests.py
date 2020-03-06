from scryfall import ScryfallCardFactory
if __name__ == '__main__':
    ds = ScryfallCardFactory(cards.cache_location('CardBack.jpg'))
    forest = ds.make_card('Forest', 'C16')
    werewolf = ds.make_card('Gatstaf Arsonists // Gatstaf Ravagers')
    print(forest.name)
    print(forest.image)
    print(forest._filename())
    print(werewolf.name)
    print(werewolf.image)
    print(werewolf._filename())
