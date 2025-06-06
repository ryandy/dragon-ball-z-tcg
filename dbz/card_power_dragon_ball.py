import sys

from dbz.card_power import CardPower
from dbz.cost import Cost


class CardPowerDragonBall(CardPower):
    def __init__(self, name, description, cost=None,
                 exhaust=True, discard=False, remove_from_game=False):
        super().__init__(name, description, cost or Cost.none(),
                         exhaust=exhaust, discard=discard, remove_from_game=remove_from_game)

    def copy(self):
        # Note: do not deep copy self.card
        return super().copy()

    def on_play(self, player, phase):
        pass
