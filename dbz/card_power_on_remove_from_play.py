import copy
import sys

from dbz.card_power import CardPower
from dbz.cost import Cost


class CardPowerOnRemoveFromPlay(CardPower):
    def __init__(self, name, description):
        super().__init__(name, description, Cost.none())

    def copy(self):
        # Note: do not deep copy self.card
        return copy.copy(self)

    # Important to have player passed in here because card_power may not have player registered
    # Called _after_ the card has been removed from play
    def on_remove_from_play(self, player):
        pass
