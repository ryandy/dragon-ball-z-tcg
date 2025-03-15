import sys

from player import Player


class State:
    def __init__(self, deck1, deck2):
        self.players = [
            Player(deck1),
            Player(deck2)]

    def __repr__(self):
        return f'{self.players[0]} vs {self.players[1]}'
