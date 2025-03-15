import pathlib
import sys

from card import Card
from saga import Saga


POWER_STAGES_LEN = 11


class PersonalityCard(Card):
    def __init__(self, name, level, saga, card_number, rarity, character,
                 is_hero, power_up_rating, power_stages, card_power):
        super().__init__(name, saga, card_number, rarity, character)
        self.level = level
        self.is_hero = is_hero
        self.power_up_rating = power_up_rating
        self.power_stages = list(power_stages)
        if len(self.power_stages) == POWER_STAGES_LEN - 1:
            self.power_stages.append(0)
        self.power_stages = list(sorted(self.power_stages))
        assert len(self.power_stages) == POWER_STAGES_LEN
        self.card_power = card_power

    def __repr__(self):
        return f'{self.name} LV{self.level}'

    def from_spec(card_module):
        return PersonalityCard(
            card_module.NAME,
            card_module.LEVEL,
            card_module.SAGA,
            card_module.CARD_NUMBER,
            card_module.RARITY,
            card_module.CHARACTER,
            card_module.IS_HERO,
            card_module.POWER_UP_RATING,
            card_module.POWER_STAGES,
            card_module.CARD_POWER)
