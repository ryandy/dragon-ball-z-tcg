import pathlib
import sys

from card import Card
from saga import Saga


POWER_STAGES_LEN = 11


class PersonalityCard(Card):
    def __init__(self, name, level, saga, card_number, rarity, character, card_text,
                 is_hero, power_up_rating, power_stages, card_power):
        super().__init__(name, saga, card_number, rarity, character, card_text)
        self.level = level
        self.is_hero = is_hero
        self.power_up_rating = power_up_rating
        self.power_stages = list(power_stages)
        if len(self.power_stages) == POWER_STAGES_LEN - 1:
            self.power_stages.append(0)
        self.power_stages = list(sorted(self.power_stages))
        assert len(self.power_stages) == POWER_STAGES_LEN
        self.card_power = card_power

        # Play state
        self.power_stage = None

    def __repr__(self):
        return f'{self.name} Lv{self.level}'

    def play_as_main(self):
        self.power_stage = 5

    def play_as_ally(self):
        self.power_stage = 3

    def power_up(self, is_ally=False, tokui_waza=None):
        if is_ally:
            increment = 1
        elif tokui_waza:
            increment = self.power_up_rating + 1
        else:
            increment = self.power_up_rating
        self.power_stage = min(self.power_stage + increment, POWER_STAGES_LEN - 1)

    def deactivate(self):
        self.power_stage = None

    def get_description(self, detailed=False, anger=None, life=None):
        description = f'{self.name} Lv{self.level}'
        if self.power_stage is None:  # Card is unplayed/inactive
            description = f'{description}, Power {self.power_stages[1]}-{self.power_stages[-1]}'
        else:
            description = (f'{description}, Power {self.power_stage}/{POWER_STAGES_LEN-1}'
                           f' ({self.power_stages[self.power_stage]})')
        if anger is not None:
            description = f'{description}, Anger {anger}/5'
        if life is not None:
            description = f'{description}, Life {life}'
        if not detailed:
            return description
        description = f'{description}\n  {self.card_text}'
        return description

    @classmethod
    def from_spec(cls, card_module):
        return cls(
            card_module.NAME,
            card_module.LEVEL,
            card_module.SAGA,
            card_module.CARD_NUMBER,
            card_module.RARITY,
            card_module.CHARACTER,
            card_module.CARD_TEXT,
            card_module.IS_HERO,
            card_module.POWER_UP_RATING,
            card_module.POWER_STAGES,
            card_module.CARD_POWER)
