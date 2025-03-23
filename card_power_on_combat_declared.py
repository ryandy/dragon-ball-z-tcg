import sys

from card_power import CardPower
from cost import Cost


class CardPowerOnCombatDeclared(CardPower):
    def __init__(self, name, description, card=None):
        super().__init__(name, description, Cost.none(), card=card)

    def copy(self):
        # Note: do not deep copy self.card
        return super().copy()

    def on_combat_declared(self, player, phase):
        pass
