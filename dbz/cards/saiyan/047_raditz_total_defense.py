import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Raditz Total Defense'
SUBTYPE = 'Physical Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '47'
RARITY = 1
DECK_LIMIT = None
CHARACTER = 'Raditz'
STYLE = None
CARD_TEXT = ('Stops a physical attack, but costs 1 power stage to perform.')

CARD_POWER = CardPowerPhysicalDefense(NAME, CARD_TEXT, cost=Cost(power=1))
