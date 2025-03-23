import sys


class State:
    TURN = 0
    COMBAT_ROUND = 0
    INTERACTIVE = False


    @classmethod
    def get_time(cls):
        return (cls.TURN, cls.COMBAT_ROUND)
