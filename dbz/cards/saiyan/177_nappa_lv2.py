import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Nappa Lv2'
LEVEL = 2
SAGA = 'Saiyan'
CARD_NUMBER = '177'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Nappa'
IS_HERO = False
POWER_UP_RATING = 3
POWER_STAGES = range(4200, 8700+1, 500)
CARD_TEXT = ('Special Physical Attack inflicting 6 stages of power drain.')

CARD_POWER = CardPowerPhysicalAttack(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
    damage=Damage(power=6))
