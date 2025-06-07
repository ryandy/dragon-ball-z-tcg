import sys

from dbz.card_power_on_damage_modification import CardPowerOnDamageModification
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Saiyan Power Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '236'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Saiyan'
RESTRICTED = False
CARD_TEXT = ('All of your physical attacks do +2 power stages of damage.')

CARD_POWER = CardPowerOnDamageModification(
    NAME, CARD_TEXT, own_physical=DamageModifier(power_add=2))
