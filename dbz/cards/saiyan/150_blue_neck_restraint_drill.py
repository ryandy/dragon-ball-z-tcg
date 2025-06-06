import sys

from dbz.card_power_on_damage_modification import CardPowerOnDamageModification
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Blue Neck Restraint Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '150'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Blue'
RESTRICTED = 'Blue'
CARD_TEXT = ('All of your physical attacks do +3 power stages of damage.'
             ' Cannot be used with any other Blue Drills in play.')

CARD_POWER = CardPowerOnDamageModification(
    NAME, CARD_TEXT, own_physical=DamageModifier(power_add=3))
