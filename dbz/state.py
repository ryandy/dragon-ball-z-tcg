import sys


class State:
    SEED = None
    RUNNER = None
    TURN = 0
    TURN_PLAYER = None
    ATTACKING_PLAYER = None
    COMBAT_ROUND = 0
    PHASE = None
    PASS_COUNT = 0
    TUTORIAL_COMPLETE = False

    IO_BACKEND = None  # set below to avoid a circular import at module load time

    QUIET = False
    ALLOW_MOST_POWERFUL_PERSONALITY_VICTORY = True
    INTERACTIVE = False
    ACK_OPPONENT_ACTIONS = False  # browser UI: block on "Continue" after opponent actions
    ROUND_KEY = None  # e.g. "1.2" while inside a combat attack round, else None
    ROUND_NEEDS_ACK = False  # an opponent action happened in the current round
    PRINT_FREQUENCY = 20  # lines per second
    MIN_PRINT_FREQUENCY = 10
    PRINT_WIDTH = 100
    MIN_PRINT_WIDTH = 80


    @classmethod
    def get_time(cls):
        return (cls.TURN, cls.COMBAT_ROUND)


    @classmethod
    def gen_players(cls):
        if cls.ATTACKING_PLAYER:
            yield cls.ATTACKING_PLAYER
            yield cls.ATTACKING_PLAYER.opponent
        else:
            yield cls.TURN_PLAYER
            yield cls.TURN_PLAYER.opponent
