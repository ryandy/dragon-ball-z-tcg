import sys

from card_power_on_draw import CardPowerOnDraw
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Red Coordination Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '144'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Red'
RESTRICTED = False
CARD_TEXT = ('When entering Combat as the defender, you may draw a card.')

CARD_POWER = CardPowerOnDraw(
    NAME, CARD_TEXT, exhaust=False, discard=False, choice=True, own_defend_draw_add=1)
