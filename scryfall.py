import urllib.parse
import urllib.request
import json
import itertools

class ScryfallCardFactory:
    def __init__(self, default_image):
        self.default_image = default_image
        self._cache = {}

    def _cache_request(self, request, transformer=lambda x: x):
        if request in self._cache:
            return self._cache[request]
        else:
            response = urllib.request.urlopen(request)
            if response.getcode() < 200 or response.getcode() > 299:
                print("HTTP Status " + response.getcode())
                return None
            response = transformer(response)
            self._cache[request] = response
            return response

    def _get_card_json(self, name, mtg_set=None):
        params = {'exact': name}
        if mtg_set is not None:
            params['set'] = mtg_set
        url = 'https://api.scryfall.com/cards/named?'
        params = urllib.parse.urlencode(params)
        request = url+params
        response = self._cache_request(request, json.load)
        return response

    def fetch_card(self, name, mtg_set=None):
        card_json = self._get_card_json(name, mtg_set)
        if card_json is None:
            return self.default_image
        if 'image_uris' in card_json:
            front_image = self._image_uri(card_json)
        else:
            #double-sided card
            front_image = self._image_uri(card_json['card_faces'][0])
        return front_image

    def fetch_related(self, name, mtg_set=None):
        related_cards = ()
        card_json = self._get_card_json(name, mtg_set)
        if card_json is None:
            return
        if 'all_parts' in card_json:
            included_types = set(("token", "meld_result"))
            for part in card_json['all_parts']:
                #TODO Get card from part as TTSCard
                yield ('Name', 'Set')

        if 'card_faces' in card_json and 'image_uris' not in card_json:
            for fact in card_json['card_faces'][1]:
            #TODO Get card face as TTSCard
                pass

    def _image_uri(self, face):
        return face['image_uris']['normal'].partition('?')[0]

if __name__ == '__main__':
    ds = ScryfallCardFactory('Image not found')
    print(ds.fetch_card('Forest', 'C16'))
    print(ds.fetch_card('Gatstaf Arsonists // Gatstaf Ravagers'))
