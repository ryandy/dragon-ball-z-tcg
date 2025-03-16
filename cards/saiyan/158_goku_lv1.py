import sys

from combat_phase import CombatPhase


TYPE = 'Personality'
NAME = 'Goku'
LEVEL = 1
SAGA = 'Saiyan'
CARD_NUMBER = 158
RARITY = 4
CHARACTER = 'Goku'
IS_HERO = True
POWER_UP_RATING = 1
POWER_STAGES = range(500, 1400+1, 100)
CARD_TEXT = ('Kamehameha Energy Attack does three life card draw and only costs one power stage to'
             ' perform.')


def CARD_POWER_CONDITION(card, player, phase):
    return isinstance(phase, CombatPhase)


def CARD_POWER(card, player, phase):
    pass
