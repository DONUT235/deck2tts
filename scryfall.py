import urllib.parse
import json
import itertools
import cards
import downloads
from datetime import timedelta

downloads.register_host('scryfall', timedelta(milliseconds=100))

class ScryfallCardFactory:
    def __init__(self, default_image):
        self.default_image = default_image

    def _get_card_json(self, name, mtg_set=None):
        params = {'exact': name}
        if mtg_set is not None:
            params['set'] = mtg_set
        url = 'https://api.scryfall.com/cards/named?'
        params = urllib.parse.urlencode(params)
        request = url+params
        response = downloads.cache_request(request, json.load)
        return response

    def _card_from_json(self, card_json, mtg_set=''):
        if 'image_uris' in card_json:
            image = self._image_uri(card_json)
            name = card_json['name']
        else:
            #double-sided card
            image = self._image_uri(card_json['card_faces'][0])
            name = card_json['card_faces'][0]['name']
        return cards.OnlineTTSCard(name, image, mtg_set)

    def make_card(self, name, mtg_set=''):
        card_json = self._get_card_json(name, mtg_set)
        if card_json is None:
            #TODO return a Card instead
            return self.default_image
        return self._card_from_json(card_json, mtg_set)

    def make_related(self, name, mtg_set=''):
        related_cards = ()
        card_json = self._get_card_json(name, mtg_set)
        if card_json is None:
            return
        if 'all_parts' in card_json:
            included_types = set(("token", "meld_result"))
            for part in card_json['all_parts']:
                other_card = downloads._cache_request(part['uri'], json.load)
                yield self._card_from_json(other_card)

        if 'card_faces' in card_json and 'image_uris' not in card_json:
            for face in range(1, len(card_json['card_faces'])):
                image = self._image_uri(card_json['card_faces'][face])
                face_name = card_json['card_faces'][face]['name']
                yield cards.OnlineTTSCard(face_name, image, mtg_set, face)

    def _image_uri(self, face):
        return face['image_uris']['normal'].partition('?')[0]
