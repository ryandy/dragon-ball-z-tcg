import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Blue Inner Leg Throw'
SUBTYPE = 'Physical Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '62'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Blue'
CARD_TEXT = ('Stops a physical attack. Lower foe\'s anger level by 1.')

CARD_POWER = CardPowerPhysicalDefense(NAME, CARD_TEXT, opp_anger=-1)
