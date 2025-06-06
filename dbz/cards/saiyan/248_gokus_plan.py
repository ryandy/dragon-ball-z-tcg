import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Goku\'s Plan'
SUBTYPE = 'Energy Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '248'
RARITY = 6
DECK_LIMIT = None
CHARACTER = 'Goku'
STYLE = None
CARD_TEXT = ('Energy attack doing 5 life cards of damage for no power cost.')

CARD_POWER = CardPowerEnergyAttack(
    NAME, CARD_TEXT, damage=Damage(life=5), cost=Cost.none())
