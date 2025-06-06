import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Goku\'s Energy Blast!'
SUBTYPE = 'Energy Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '153'
RARITY = 3
DECK_LIMIT = None
CHARACTER = 'Goku'
STYLE = None
CARD_TEXT = ('Energy defense stopping a foe\'s physical attack. Remove from the game after use.')

CARD_POWER = CardPowerPhysicalDefense(NAME, CARD_TEXT, remove_from_game=True)
