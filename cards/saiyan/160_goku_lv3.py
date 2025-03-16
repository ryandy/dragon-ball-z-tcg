import sys

from combat_phase import CombatPhase


TYPE = 'Personality'
NAME = 'Goku'
LEVEL = 3
SAGA = 'Saiyan'
CARD_NUMBER = 160
RARITY = 4
CHARACTER = 'Goku'
IS_HERO = True
POWER_UP_RATING = 3
POWER_STAGES = range(8000, 12500+1, 500)
CARD_TEXT = ('Prevent 2 life card draws from being discarded from a successful energy attack.')


def CARD_POWER_CONDITION(card, player, phase):
    return isinstance(phase, CombatPhase)


def CARD_POWER(card, player, phase):
    pass
