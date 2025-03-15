from importlib.machinery import SourceFileLoader
import pathlib
import sys

from combat_card import CombatCard
from personality_card import PersonalityCard
from saga import Saga


class CardFactory:
    @staticmethod
    def from_spec(saga, card_number):
        path = pathlib.Path(f'./cards/{Saga(saga).name}'.lower())
        files = list(path.glob(f'{card_number}_*.py'))
        if len(files) != 1:
            return None
        filename = files[0]
        card_module = SourceFileLoader('card_module', str(filename)).load_module()
        if card_module.TYPE.lower() == 'personality':
            return PersonalityCard.from_spec(card_module)
        if card_module.TYPE.lower() == 'combat':
            return CombatCard.from_spec(card_module)
