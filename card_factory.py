from importlib.machinery import SourceFileLoader
import pathlib
import sys


from personality_card import PersonalityCard
from saga import Saga


class CardFactory:
    @staticmethod
    def from_spec(saga, card_number):
        path = pathlib.Path(f'./cards/{Saga.to_string(saga)}')
        files = list(path.glob(f'{card_number}_*.py'))
        if len(files) != 1:
            return None
        filename = files[0]
        card_module = SourceFileLoader('card_module', str(filename)).load_module()
        if card_module.TYPE == 'Personality':
            return PersonalityCard.from_spec(card_module)
