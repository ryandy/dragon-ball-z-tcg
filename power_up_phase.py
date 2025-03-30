import sys

from phase import Phase
from state import State


class PowerUpPhase(Phase):
    def __init__(self, player):
        self.player = player

    def execute(self):
        State.PHASE = self

        self.player.main_personality.power_up(tokui_waza=self.player.tokui_waza)
        for ally in self.player.allies:
            ally.power_up(is_ally=True)

        # TODO: CardPowerOnEndOfPowerUp
        #       213 Plant Two Saibaimen
