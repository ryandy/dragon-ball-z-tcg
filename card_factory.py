from importlib.machinery import SourceFileLoader
import pathlib
import sys

from combat_card import CombatCard
from dragon_ball_card import DragonBallCard
from drill_card import DrillCard
from non_combat_card import NonCombatCard
from personality_card import PersonalityCard
from saga import Saga


class CardFactory:
    @staticmethod
    def from_spec(saga, card_number):
        saga_name = f'{Saga(saga).name}'.lower()
        path = pathlib.Path(f'./cards/{saga_name}')
        files = list(path.glob(f'{card_number}_*.py'))
        if len(files) != 1:
            print(f'Warning: Could not find card at {path}')
            return None
        filename = files[0]
        module_name = '{saga_name}_{card_number}'
        card_module = SourceFileLoader(module_name, str(filename)).load_module()
        if card_module.TYPE.lower() == 'personality':
            return PersonalityCard.from_spec(card_module)
        if card_module.TYPE.lower() == 'combat':
            return CombatCard.from_spec(card_module)
        if card_module.TYPE.lower() == 'non-combat':
            return NonCombatCard.from_spec(card_module)
        if card_module.TYPE.lower() == 'dragon ball':
            return DragonBallCard.from_spec(card_module)
        if card_module.TYPE.lower() == 'drill':
            return DrillCard.from_spec(card_module)
