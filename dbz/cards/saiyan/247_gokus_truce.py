import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerAnyDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Goku\'s Truce'
SUBTYPE = 'Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '247'
RARITY = 6
DECK_LIMIT = None
CHARACTER = 'Goku'
STYLE = None
CARD_TEXT = ('Stops a successful energy or physical attack.')

CARD_POWER = CardPowerAnyDefense(NAME, CARD_TEXT)
