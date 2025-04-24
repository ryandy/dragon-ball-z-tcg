import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Saiyan Energy Throw'
SUBTYPE = 'Energy Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '91'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Saiyan'
CARD_TEXT = ('Saiyan heritage only. Energy attack doing 7 life card draws at a cost of'
             ' 4 stages of power drain. Remove from the game after use.')

CARD_POWER = CardPowerEnergyAttack(
    NAME, CARD_TEXT,
    damage=Damage(life=7), cost=Cost(power=4),
    saiyan_only=True, remove_from_game=True)
