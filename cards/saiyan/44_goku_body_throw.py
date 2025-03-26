import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Goku Body Throw'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '44'
RARITY = 1
DECK_LIMIT = None
CHARACTER = 'Goku'
STYLE = None
CARD_TEXT = ('Physical attack doing 1 life card of damage.')

CARD_POWER = CardPowerPhysicalAttack(NAME, CARD_TEXT, damage=Damage(life=1))
