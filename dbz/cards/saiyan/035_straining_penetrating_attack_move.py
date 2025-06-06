import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Straining, Penetrating Attack Move'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '35'
RARITY = 1
DECK_LIMIT = 1
CHARACTER = None
STYLE = None
CARD_TEXT = ('Physical attack forcing the defender to lose 3 life cards and the attacker'
             ' 3 stages of power.')

CARD_POWER = CardPowerPhysicalAttack(NAME, CARD_TEXT, cost=Cost(power=3), damage=Damage(life=3))
