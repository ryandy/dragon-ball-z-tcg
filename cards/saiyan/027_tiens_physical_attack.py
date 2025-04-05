import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Tien\'s Physical Attack'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '27'
RARITY = 1
DECK_LIMIT = None
CHARACTER = 'Tien'
STYLE = None
CARD_TEXT = ('Physical attack doing 5 life card draws if successful.')

CARD_POWER = CardPowerPhysicalAttack(NAME, CARD_TEXT, damage=Damage(life=5))
