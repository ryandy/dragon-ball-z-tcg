import copy
import sys

from card_power import CardPower
from cost import Cost
from util import dprint


class CardPowerOnDamageApplied(CardPower):
    def __init__(self, name, description,
                 choice=False, exhaust=True, exhaust_until_next_turn=False,
                 discard=True, remove_from_game=False):
        super().__init__(name, description, Cost.none())
        self.choice = choice
        self.exhaust = exhaust
        self._exhaust_until_next_turn = exhaust_until_next_turn
        self.discard = discard
        self.remove_from_game = remove_from_game

    def copy(self):
        # Note: do not deep copy self.card
        return copy.copy(self)

    def on_damage_applied(self, damaged_player, power_damage=None, life_damage=None):
        if (self.on_condition(damaged_player, power_damage, life_damage)
            and (not self.choice or self.player.choose_to_use_card_power(self))):
            dprint(f'{self.player} uses {self}')
            dprint(f'  - {self.description}')
            self.on_effect(damaged_player, power_damage, life_damage)
            self.on_resolved()

    def on_condition(self, damaged_player, power_damage, life_damage):
        return True

    def on_effect(self, damaged_player, power_damage, life_damage):
        pass

    def on_resolved(self):
        if self._exhaust_until_next_turn:
            if self.card:
                self.player.exhaust_card_until_next_turn(self.card)
            else:
                self.exhaust_until_next_turn()
        elif self.exhaust:
            if self.card:
                self.player.exhaust_card(self.card)
            else:
                self.player.exhaust_card_power(self)

        if self.card:
            if self.remove_from_game:
                self.player.remove_from_game(self.card, exhaust_card=False)
            elif self.discard:
                self.player.discard(self.card, exhaust_card=False)
