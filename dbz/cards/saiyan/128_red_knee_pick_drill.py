import sys

from dbz.card_power_on_draw import CardPowerOnDraw
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Red Knee Pick Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '128'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Red'
RESTRICTED = False
CARD_TEXT = ('When entering Combat as the attacker, you may draw a card.')

CARD_POWER = CardPowerOnDraw(
    NAME, CARD_TEXT, exhaust=False, discard=False, choice=True, own_attack_draw_add=1)
