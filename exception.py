import sys


class GameOver(Exception):
    def __init__(self, message, winning_player):
        super().__init__(message)
        self.winning_player = winning_player
