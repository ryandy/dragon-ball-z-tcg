import sys

from dbz.card_power import CardPower
from dbz.cost import Cost
from dbz.util import dprint


class CardPowerOnEnteringCombat(CardPower):
    def __init__(self, name, description, card=None,
                 choice=False, exhaust=True, discard=True, remove_from_game=False):
        super().__init__(name, description, Cost.none(), card=card,
                         exhaust=exhaust, discard=discard, remove_from_game=remove_from_game)
        self.choice = choice

    def copy(self):
        # Note: do not deep copy self.card
        return super().copy()

    def on_entering_combat(self, phase):
        if (self.on_condition(phase)
            and (not self.choice or self.player.choose_to_use_card_power(self))):
            dprint(f'{self.player} uses {self}')
            dprint(f'  - {self.description}')
            self.on_effect(phase)
            self.on_resolved()

    def on_condition(self, phase):
        return True

    def on_effect(self, phase):
        pass
