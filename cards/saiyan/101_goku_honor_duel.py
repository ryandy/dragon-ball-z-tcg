import sys

from card_power_attack import CardPowerNonCombatAttack
from card_power_on_draw import CardPowerOnDraw
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Goku Honor Duel!'
SAGA = 'Saiyan'
CARD_NUMBER = '101'
RARITY = 3
DECK_LIMIT = None
CHARACTER = 'Goku'
STYLE = None
CARD_TEXT = ('Use when entering Combat as the defender. Instead of drawing 3 cards from your life '
             'deck, draw the bottom 3 cards from your discard pile. Remove from the game after use')

CARD_POWER = CardPowerOnDraw(
    NAME, CARD_TEXT, remove_from_game=True,
    own_defend_draw_add=-3,
    own_defend_draw_from_discard_add=3)
