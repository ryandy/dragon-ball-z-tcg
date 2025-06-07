import sys

from dbz.card_power_on_damage_modification import CardPowerOnDamageModification
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Black Shadow Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '235'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Black'
RESTRICTED = False
CARD_TEXT = ('Allows the card owner to take 2 less power stages of power drain from'
             ' a successful physical attack.')

CARD_POWER = CardPowerOnDamageModification(
    NAME, CARD_TEXT, opp_physical=DamageModifier(power_add=-2))
