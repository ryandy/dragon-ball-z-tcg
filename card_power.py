import abc
import sys

from state import State


class CardPower(abc.ABC):
    def __init__(self, name, description, cost, card=None, is_floating=False):
        self.name = name
        self.description = description
        self.cost = cost
        self.card = card
        self.is_floating = is_floating
        self.valid_from = None  # tuple of (turn #, combat phase #)
        self.valid_until = None

    def register_card(self, card):
        self.card = card

    def set_floating(self):
        self.is_floating = True

    def exhaust_until_next_turn(self):
        self.valid_from = (State.TURN + 1, 0)

    def exhaust_after_next_combat_phase(self):
        self.valid_until = (State.TURN, State.COMBAT_ROUND + 1)

    def is_exhausted(self):
        cur_time = State.get_time()
        valid = ((not self.valid_from or self.valid_from <= cur_time)
                 and (not self.valid_until or cur_time <= self.valid_until))
        return not valid
