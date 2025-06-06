import sys

from dbz.card_power_defense_shield import CardPowerAnyDefenseShield
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Piccolo\'s Flight'
SAGA = 'Saiyan'
CARD_NUMBER = '212'
RARITY = 5
DECK_LIMIT = None
CHARACTER = 'Piccolo'
STYLE = None
CARD_TEXT = ('Defense Shield: Stop the first unstopped energy or physical attack performed'
             ' against you.')

CARD_POWER = CardPowerAnyDefenseShield(NAME, CARD_TEXT)
