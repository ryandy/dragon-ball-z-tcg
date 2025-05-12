import sys

from card_power_attack import CardPowerPhysicalAttack, CardPowerEnergyAttack
from card_power_on_draw import CardPowerOnDraw
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Gohan Lv4'
LEVEL = 4
SAGA = 'Saiyan'
CARD_NUMBER = 'P5'
RARITY = 2
DECK_LIMIT = 1
CHARACTER = 'Gohan'
IS_HERO = True
POWER_UP_RATING = 4
POWER_STAGES = range(3200, 7700+1, 500)
CARD_TEXT = ('Draws an extra card from the bottom of the discard pile for this combat.')

# TODO: Should this be OnEnteringCombat like #182 Krillin HT Lv1?
#       It effects which cards are in hand when deciding whether to declare combat
CARD_POWER = CardPowerOnDraw(
    NAME, CARD_TEXT, exhaust=False, discard=False,
    own_attack_draw_from_discard_add=1,
    own_defend_draw_from_discard_add=1)
