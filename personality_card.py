import bisect
import pathlib
import sys

from card import Card
from saga import Saga


POWER_STAGES_LEN = 11

PHYSICAL_ATTACK_TABLE_VALUES = [0, 100, 600, 1000, 3000, 10000, 15500, 25000]


class PersonalityCard(Card):
    def __init__(self, name, level, saga, card_number, rarity, deck_limit, character, card_text,
                 is_hero, power_up_rating, power_stages, card_power):
        style = None
        super().__init__(name, saga, card_number, rarity, deck_limit, character, style,
                         card_text, card_power)
        self.level = level
        self.is_hero = is_hero
        self.power_up_rating = power_up_rating
        self.power_stages = list(power_stages)
        if len(self.power_stages) == POWER_STAGES_LEN - 1:
            self.power_stages.append(0)
        self.power_stages = list(sorted(self.power_stages))
        assert len(self.power_stages) == POWER_STAGES_LEN

        # Play state
        self.power_stage = None

    def __repr__(self):
        return f'{self.name} Lv{self.level} (Personality)'

    def init_power_stage_for_main(self):
        self.set_power_stage(5)

    def init_power_stage_for_ally(self):
        self.set_power_stage(3)

    def reduce_power_stage(self, amount):
        self.adjust_power_stage(-amount)

    def adjust_power_stage(self, amount):
        self.set_power_stage(min(POWER_STAGES_LEN - 1, max(0, self.power_stage + amount)))

    def set_power_stage(self, new_power_stage):
        self.power_stage = new_power_stage

    def set_power_stage_max(self):
        self.set_power_stage(POWER_STAGES_LEN - 1)

    def get_power(self):
        if self.power_stage is None:
            return None
        return self.power_stages[self.power_stage]

    def get_physical_attack_table_index(self):
        power = self.get_power()
        if power is None:
            return 0
        index = bisect.bisect_right(PHYSICAL_ATTACK_TABLE_VALUES, power) - 1
        return index

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

    @classmethod
    def from_spec(cls, card_module):
        card = cls(
            card_module.NAME,
            card_module.LEVEL,
            card_module.SAGA,
            card_module.CARD_NUMBER,
            card_module.RARITY,
            card_module.DECK_LIMIT,
            card_module.CHARACTER,
            card_module.CARD_TEXT,
            card_module.IS_HERO,
            card_module.POWER_UP_RATING,
            card_module.POWER_STAGES,
            card_module.CARD_POWER)
        for card_power in card.card_powers:
            card_power.register_card(card)
        return card
