import copy
import sys

from card_power import CardPower
from cost import Cost
from util import dprint


class CardPowerOnAttackResolved(CardPower):
    def __init__(self, name, description,
                 choice=False, exhaust=True, exhaust_until_next_turn=False,
                 silent=False,
                 discard=True, remove_from_game=False):
        super().__init__(name, description, Cost.none(),
                         exhaust=exhaust, exhaust_until_next_turn=exhaust_until_next_turn,
                         discard=discard, remove_from_game=remove_from_game)
        self.choice = choice
        self.silent = silent

    def copy(self):
        # Note: do not deep copy self.card
        return copy.copy(self)

    def on_attack_resolved(self, phase, damage, is_physical):
        if (self.on_condition(phase, damage, is_physical)
            and (not self.choice or self.player.choose_to_use_card_power(self))):
            if not self.silent:
                dprint(f'{self.player} uses {self}')
                dprint(f'  - {self.description}')
            self.on_effect(phase, damage, is_physical)
            self.on_resolved()

    def on_condition(self, phase, damage, is_physical):
        return True

    def on_effect(self, phase, damage, is_physical):
        pass
