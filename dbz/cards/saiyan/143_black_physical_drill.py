import sys

from dbz.card_power_on_damage_modification import CardPowerOnDamageModification
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Black Physical Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '143'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Black'
RESTRICTED = 'Black'
CARD_TEXT = ('All physical attacks performed against you do 1 less power stage of damage.'
             ' Can\'t be used with any other Black Drills in play.')

CARD_POWER = CardPowerOnDamageModification(
    NAME, CARD_TEXT, opp_physical=DamageModifier(power_add=-1))
