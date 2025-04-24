import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Yajirobe\'s Energy Attack'
SUBTYPE = 'Energy Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '122'
RARITY = 3
DECK_LIMIT = None
CHARACTER = 'Yajirobe'
STYLE = None
CARD_TEXT = ('Energy attack forcing 1 life card of damage. Remove from the game after use.')

CARD_POWER = CardPowerEnergyAttack(NAME, CARD_TEXT, damage=Damage(life=1), remove_from_game=True)
