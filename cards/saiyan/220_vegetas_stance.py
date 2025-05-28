import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Vegeta\'s Stance'
SUBTYPE = 'Energy Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '220'
RARITY = 5
DECK_LIMIT = None
CHARACTER = 'Vegeta'
STYLE = None
CARD_TEXT = ('Prevents all but 1 life card draw from a successful energy attack.'
             ' Remove from the game after use.')

CARD_POWER = CardPowerEnergyDefense(
    NAME, CARD_TEXT, remove_from_game=True,
    damage_modifier=DamageModifier(life_prevent=-1))
