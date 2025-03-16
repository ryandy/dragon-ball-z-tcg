import sys


class LossError(Exception):
    def __init__(self, message, player):
        super().__init__(message)
        self.player = player
