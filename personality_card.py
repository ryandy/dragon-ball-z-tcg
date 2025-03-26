import bisect
import pathlib
import sys

from card import Card
from saga import Saga
from state import State
from util import dprint


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
        self.covered_ally = None  # When an ally overlays another, point to the covered one
        self.play_turn = None

    def __repr__(self):
        return f'{self.name} (Personality)'

    def char_name(self):
        return f'{self.character.name.title().replace("_", "-")}'

    def get_name_level(self):
        return f'{self.character.name}.{self.level}'

    def init_for_main(self):
        self.play_turn = State.TURN
        self.set_power_stage(5)

    def init_for_ally(self, covered_ally=None):
        self.play_turn = State.TURN
        self.set_power_stage(3)
        self.covered_ally = covered_ally
        if covered_ally:
            self.set_power_stage_max()

    def reduce_power_stage(self, amount):
        self.adjust_power_stage(-amount)

    def adjust_power_stage(self, amount):
        new_power = min(POWER_STAGES_LEN - 1, max(0, self.power_stage + amount))
        delta = new_power - self.power_stage
        if delta:
            verb = 'increases' if delta > 0 else 'decreases'
            old_str = self.get_power_attack_str()
            new_str = self.get_power_attack_str(power_stage=new_power)
            dprint(f'{self.name}\'s power {verb} from {old_str} to {new_str}')
        self.set_power_stage(new_power)

    def set_power_stage(self, new_power_stage):
        self.power_stage = new_power_stage

    def set_power_stage_max(self):
        self.adjust_power_stage(POWER_STAGES_LEN - 1)

    def get_power(self, power_stage=None):
        if power_stage is None:
            power_stage = self.power_stage
        if power_stage is None:
            return None
        return self.power_stages[power_stage]

    def get_physical_attack_table_index(self, power_stage=None):
        power = self.get_power(power_stage=power_stage)
        if power is None:
            return 0
        index = bisect.bisect_right(PHYSICAL_ATTACK_TABLE_VALUES, power) - 1
        return index

    def get_physical_attack_table_index_max(self):
        return self.get_physical_attack_table_index(power_stage=POWER_STAGES_LEN-1)

    def get_power_attack_str(self, power_stage=None):
        if power_stage is None:
            power_stage = self.power_stage
        pat_idx = self.get_physical_attack_table_index(power_stage=power_stage)
        return f'{power_stage}({pat_idx})'

    def power_up(self, is_ally=False, tokui_waza=None):
        if is_ally:
            increment = 1
        elif tokui_waza:
            increment = self.power_up_rating + 1
        else:
            increment = self.power_up_rating
        self.adjust_power_stage(increment)

    def can_be_played(self, player):
        is_overlay = any(
            (x.character == self.character and x.level == self.level - 1)
            for x in player.allies)

        # Cannot be a different hero/villain status than Main Personality
        hero_restricted = self.is_hero != player.main_personality.is_hero

        # Cannot be the same character as your Main Personality
        mp_restricted = self.character == player.main_personality.character

        # Cannot be a higher level than Main Personality unless overlaying
        level_restricted = not is_overlay and (self.level > player.main_personality.level)

        # Cannot be a higher level than MP's highest level minus 2
        max_level_restricted = self.level > len(player.main_personalities) - 2

        # Cannot be the same character as an ally you have in play unless overlaying
        # TODO: Saibaimen exception
        char_restricted = not is_overlay and any(
            x.character == self.character for x in player.allies)

        return (not hero_restricted
                and not mp_restricted
                and not level_restricted
                and not max_level_restricted
                and not char_restricted)

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
