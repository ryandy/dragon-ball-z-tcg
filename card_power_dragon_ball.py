import sys

from card_power import CardPower
from cost import Cost


class CardPowerDragonBall(CardPower):
    def __init__(self, name, description, cost=None):
        super().__init__(name, description, cost or Cost.none())

    def on_play(self, player, phase):
        pass
