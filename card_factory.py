from importlib.machinery import SourceFileLoader
import pathlib
import re
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
        card_number = str(card_number).lower()
        saga_name = f'{Saga(saga).name}'.lower()
        path = pathlib.Path(f'./cards/{saga_name}')
        files = list(path.glob(f'*{card_number}_*.py'))

        cardfile = None
        for f in files:
            if re.match(f'0*{card_number}_', f.name):
                cardfile = f
                break

        if cardfile is None:
            print(f'Warning: Could not find card {card_number} at {path}')
            return None

        return CardFactory.from_file(cardfile)

    @staticmethod
    def from_file(cardfile):
        match = re.match(r'.*/(\w+)/(\w+)_', str(cardfile))
        saga_name = match.group(1)
        card_number = match.group(2)
        module_name = f'{saga_name}_{card_number}'
        card_module = SourceFileLoader(module_name, str(cardfile)).load_module()
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

    @staticmethod
    def from_card(card):
        return CardFactory.from_spec(card.saga, card.card_number)
