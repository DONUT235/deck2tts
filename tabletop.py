#TODO write toJSON methods in each of these
#as well as in TTSCard
class TTSDeck:
    def __init__(self):
        self.main = TTSSingleDeck()
        self.side = TTSSingleDeck()
        self.extra = TTSExtraDeck()
        self.command_zone = TTSExtraDeck()

    def get_main_count(self, card):
        return self.main.get_count(card)

    def get_side_count(self, card):
        return self.side.get_count(card)

    def in_extra(self, card):
        return self.extra.has_card(card)

    def is_commander(self, card):
        return self.command_zone.has_card(card)

    def add_main(self, card, count=1):
        self.main.add_card(card, count)

    def add_side(self, card, count=1):
        self.side.add_card(card, count)

    def add_commander(self, card):
        self.command_zone.add_card(card)

    def add_extra(self, card):
        self.extra.add_card(card)


class TTSSingleDeck:
    def __init__(self):
        self.cards = {}

    def add_card(self, card, count):
        if card in self.cards:
            self.cards[card] += count
        else:
            self.cards[card] = count

    def get_count(self, card):
        if card in self.cards:
            return self.cards[card]
        else:
            return 0

class TTSExtraDeck:
    def __init__(self):
        self.cards = set()

    def add_card(self, card):
        self.cards.add(card)

    def has_card(self, card):
        return card in self.cards
