import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Saiyan Energy Defense'
SUBTYPE = 'Energy Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '92'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Saiyan'
CARD_TEXT = ('Saiyan heritage only. Stops an energy attack.')

CARD_POWER = CardPowerEnergyDefense(NAME, CARD_TEXT, saiyan_only=True)
