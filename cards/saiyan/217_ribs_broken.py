import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Ribs Broken'
SUBTYPE = 'Energy Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '217'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Energy attack doing 5 life cards of damage. Costs 0 power stages to perform. You must'
             ' remove an Ally in play from the game in order to perform this attack. This does not'
             ' have to be an Ally you control.')

CARD_POWER = CardPowerEnergyAttack(
    NAME, CARD_TEXT, damage=Damage(life=5), cost=Cost(any_ally=1))
