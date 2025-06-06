import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Straining Fake Left Move'
SUBTYPE = 'Physical Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '36'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Defensive move preventing up to 3 energy life cards from being discarded and'
             ' draining the user 4 stages.')

CARD_POWER = CardPowerEnergyDefense(
    NAME, CARD_TEXT, cost=Cost(power=4), damage_modifier=DamageModifier(life_prevent=3))
