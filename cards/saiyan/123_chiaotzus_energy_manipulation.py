import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Chiaotzu\'s Energy Manipulation'
SUBTYPE = 'Energy Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '123'
RARITY = 3
DECK_LIMIT = 1
CHARACTER = 'Chiaotzu'
STYLE = None
CARD_TEXT = ('Energy attack forcing 3 life cards of damage. Remove from the game after use.')

CARD_POWER = CardPowerEnergyAttack(NAME, CARD_TEXT, damage=Damage(life=3), remove_from_game=True)
