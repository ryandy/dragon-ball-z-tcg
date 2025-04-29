import sys


class State:
    TURN = 0
    COMBAT_ROUND = 0
    PHASE = None
    ALLOW_MOST_POWERFUL_PERSONALITY_VICTORY = True

    INTERACTIVE = False
    PRINT_FREQUENCY = 15  # lines per second
    PRINT_WIDTH = 100


    @classmethod
    def get_time(cls):
        return (cls.TURN, cls.COMBAT_ROUND)
