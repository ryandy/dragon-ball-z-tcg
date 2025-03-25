import sys

from phase import Phase


class PowerUpPhase(Phase):
    def __init__(self, player):
        self.player = player

    def execute(self):
        self.player.main_personality.power_up(tokui_waza=self.player.tokui_waza)
        for ally in self.player.allies:
            ally.power_up(is_ally=True)
