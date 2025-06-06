import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Yamcha\'s Energy Attack'
SUBTYPE = 'Energy Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '115'
RARITY = 3
DECK_LIMIT = None
CHARACTER = 'Yamcha'
STYLE = None
CARD_TEXT = ('Energy attack doing 2 life card draws of damage. Costs 3 power stages to perform.')

CARD_POWER = CardPowerEnergyAttack(NAME, CARD_TEXT, cost=Cost(power=3), damage=Damage(life=2))
