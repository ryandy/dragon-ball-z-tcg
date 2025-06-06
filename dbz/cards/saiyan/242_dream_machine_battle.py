import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerAnyDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


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
