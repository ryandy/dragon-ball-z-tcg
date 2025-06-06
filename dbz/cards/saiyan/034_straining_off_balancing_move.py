import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Straining Off-Balancing Move'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '34'
RARITY = 1
DECK_LIMIT = 1
CHARACTER = None
STYLE = None
CARD_TEXT = ('Physical attack forcing the defender to lose 1 life card and the attacker'
             ' 3 stages of power.')

CARD_POWER = CardPowerPhysicalAttack(NAME, CARD_TEXT, cost=Cost(power=3), damage=Damage(life=1))
