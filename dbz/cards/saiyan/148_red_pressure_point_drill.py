import sys

from dbz.card_power_on_damage_modification import CardPowerOnDamageModification
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Red Pressure Point Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '148'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Red'
RESTRICTED = 'Red'
CARD_TEXT = ('All of your energy attacks do +1 life cards of damage.'
             ' Cannot be used with other Red Drills in play.')

CARD_POWER = CardPowerOnDamageModification(
    NAME, CARD_TEXT, own_energy=DamageModifier(life_add=1))
