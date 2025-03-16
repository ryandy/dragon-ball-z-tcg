import sys

from phase import Phase


class DrawPhase(Phase):
    def __init__(self, player):
        self.player = player

    def execute(self):
        for _ in range(3):
            self.player.draw()
