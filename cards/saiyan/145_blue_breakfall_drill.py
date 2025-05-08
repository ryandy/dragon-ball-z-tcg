import sys

from card_power_on_damage_modification import CardPowerOnDamageModification
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Blue Breakfall Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '145'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Blue'
RESTRICTED = False
CARD_TEXT = ('All physical attacks performed against you do 2 less power stages of damage.')

CARD_POWER = CardPowerOnDamageModification(
    NAME, CARD_TEXT, opp_physical=DamageModifier(power_add=-2))
