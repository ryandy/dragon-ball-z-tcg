import sys


class GameOver(Exception):
    def __init__(self, message, winning_player):
        super().__init__(message)
        self.winning_player = winning_player


class DeckEmpty(Exception):
    def __init__(self, last_card):
        super().__init__()
        self.last_card = last_card
