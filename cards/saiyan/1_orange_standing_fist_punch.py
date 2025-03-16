import sys

from combat_phase import CombatPhase


TYPE = 'Combat'
NAME = 'Orange Standing Fist Punch'
SAGA = 'Saiyan'
CARD_NUMBER = 1
RARITY = 1
CHARACTER = 'Raditz'
STYLE = 'Orange'
IS_PHYSICAL = True
IS_ATTACK = True
CARD_TEXT = ('Physical Attack. Raise card user\'s anger level 1.')


def CARD_POWER_CONDITION(card, player, phase):
    return isinstance(phase, CombatPhase)


def CARD_POWER(card, player, phase):
    phase.physical_attack(from_card=card)
    player.raise_anger(1)
