import sys


class State:
    TURN = 0
    COMBAT_ROUND = 0
    ENABLE_INTERACTIVE = True # False

    @classmethod
    def get_time(cls):
        return (cls.TURN, cls.COMBAT_ROUND)
