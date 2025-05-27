import sys

from card_power import CardPower
from cost import Cost
from util import dprint


class CardPowerOnEnteringTurn(CardPower):
    def __init__(self, name, description, card=None,
                 choice=False, exhaust=True, discard=True, remove_from_game=False):
        super().__init__(name, description, Cost.none(), card=card,
                         exhaust=exhaust, discard=discard, remove_from_game=remove_from_game)
        self.choice = choice

    def copy(self):
        # Note: do not deep copy self.card
        return super().copy()

    def on_entering_turn(self):
        if (self.on_condition()
            and (not self.choice or self.player.choose_to_use_card_power(self))):
            dprint(f'{self.player} uses {self}')
            dprint(f'  - {self.description}')
            self.on_effect()
            self.on_resolved()

    def on_condition(self):
        return True

    def on_effect(self):
        pass
