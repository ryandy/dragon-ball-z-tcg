import sys

from dbz.card_power_on_damage_modification import CardPowerOnDamageModification
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Krillin\'s Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '215'
RARITY = 5
DECK_LIMIT = None
CHARACTER = 'Krillin'
STYLE = None
RESTRICTED = False
CARD_TEXT = ('Does an extra life card of damage with each successful attack.')

CARD_POWER = CardPowerOnDamageModification(
    NAME, CARD_TEXT, own_physical=DamageModifier(life_add=1), own_energy=DamageModifier(life_add=1))
