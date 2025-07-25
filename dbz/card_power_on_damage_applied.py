import copy
import sys

from dbz.card_power import CardPower
from dbz.cost import Cost
from dbz.util import dprint


class CardPowerOnDamageApplied(CardPower):
    def __init__(self, name, description,
                 choice=False, exhaust=True, exhaust_until_next_turn=False,
                 card=None, silent=False,
                 discard=True, remove_from_game=False):
        super().__init__(name, description, Cost.none(),
                         exhaust=exhaust, exhaust_until_next_turn=exhaust_until_next_turn,
                         card=card, discard=discard, remove_from_game=remove_from_game)
        self.choice = choice
        self.silent = silent

    def copy(self):
        # Note: do not deep copy self.card
        return copy.copy(self)

    def on_damage_applied(self, damaged_player, power_damage=None, life_damage=None):
        if (self.on_condition(damaged_player, power_damage, life_damage)
            and (not self.choice or self.player.choose_to_use_card_power(self))):
            if not self.silent:
                dprint(f'{self.player} uses {self}')
                dprint(f'  - {self.description}')
            self.on_effect(damaged_player, power_damage, life_damage)
            self.on_resolved()

    def on_condition(self, damaged_player, power_damage, life_damage):
        return True

    def on_effect(self, damaged_player, power_damage, life_damage):
        pass
