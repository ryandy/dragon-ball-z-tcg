import copy
import sys

from card_power import CardPower
from cost import Cost


class CardPowerOnDraw(CardPower):
    def __init__(self, name, description, own_draw_add=None, opp_draw_add=None,
                 own_draw_from_discard_add=None):
        super().__init__(name, description, Cost.none())
        self.own_draw_add = own_draw_add or 0
        self.opp_draw_add = opp_draw_add or 0
        self.own_draw_from_discard_add = own_draw_from_discard_add or 0

    def copy(self):
        # Note: do not deep copy self.card
        return copy.copy(self)

    def on_draw(self, phase):
        if self.player is phase.player:
            phase.draw_count += self.own_draw_add
            phase.discard_pile_draw_count += self.own_draw_from_discard_add
        else:
            phase.draw_count += self.opp_draw_add
