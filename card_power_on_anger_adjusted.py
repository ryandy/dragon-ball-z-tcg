import copy
import sys

from card_power import CardPower
from cost import Cost
from util import dprint


class CardPowerOnAngerAdjusted(CardPower):
    def __init__(self, name, description,
                 choice=False, exhaust=True, exhaust_until_next_turn=False,
                 discard=True, remove_from_game=False):
        super().__init__(name, description, Cost.none(),
                         exhaust=exhaust, exhaust_until_next_turn=exhaust_until_next_turn,
                         discard=discard, remove_from_game=remove_from_game)
        self.choice = choice

    def copy(self):
        # Note: do not deep copy self.card
        return copy.copy(self)

    # Return new anger delta
    def on_anger_adjusted(self, adjusted_player, amount):
        if (self.on_condition(adjusted_player, amount)
            and (not self.choice or self.player.choose_to_use_card_power(self))):
            dprint(f'{self.player} uses {self}')
            dprint(f'  - {self.description}')
            ret = self.on_effect(adjusted_player, amount)
            self.on_resolved()
            return ret
        return amount

    def on_condition(self, adjusted_player, amount):
        return True

    def on_effect(self, adjusted_player, amount):
        return amount
