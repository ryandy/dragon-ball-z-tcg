import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Nappa Lv4'
LEVEL = 4
SAGA = 'Saiyan'
CARD_NUMBER = 'P7'
RARITY = 2
DECK_LIMIT = 1
CHARACTER = 'Nappa'
IS_HERO = False
POWER_UP_RATING = 4
POWER_STAGES = range(14000, 23000+1, 1000)
CARD_TEXT = ('Negate a foe\'s energy attack.')

CARD_POWER = CardPowerEnergyDefense(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False)
