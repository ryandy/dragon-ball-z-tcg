import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Dream Machine Battle'
SUBTYPE = 'Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '242'
RARITY = 5
DECK_LIMIT = 0
CHARACTER = None
STYLE = None
CARD_TEXT = ('This battle never happened. Start all over with new cards and reset all damage to'
             ' beginning levels.')

# This card was never used or understood. It's banned and doesn't do anything here.
CARD_POWER = CardPowerAnyDefense(NAME, CARD_TEXT, damage_modifier=DamageModifier.none())
