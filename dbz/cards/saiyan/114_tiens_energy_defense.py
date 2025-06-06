import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Tien\'s Energy Defense'
SUBTYPE = 'Energy Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '114'
RARITY = 3
DECK_LIMIT = None
CHARACTER = 'Tien'
STYLE = None
CARD_TEXT = ('Prevents a foe\'s energy attack.')

CARD_POWER = CardPowerEnergyDefense(NAME, CARD_TEXT)
