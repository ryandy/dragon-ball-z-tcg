import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Red Side Kick'
SUBTYPE = 'Energy Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '56'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Red'
CARD_TEXT = ('Stop foe\'s energy attack this round.')

CARD_POWER = CardPowerEnergyDefense(NAME, CARD_TEXT)
