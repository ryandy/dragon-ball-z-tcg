import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Straining Head Lock Move'
SUBTYPE = 'Physical Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '41'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Stops a physical attack, but you have to discard another card to use this one.')

CARD_POWER = CardPowerPhysicalDefense(NAME, CARD_TEXT, cost=Cost(discard=1))
