import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Nappa Lv3'
LEVEL = 3
SAGA = 'Saiyan'
CARD_NUMBER = '178'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Nappa'
IS_HERO = False
POWER_UP_RATING = 4
POWER_STAGES = range(9000, 13500+1, 500)
CARD_TEXT = ('Reduce the damage from a physical attack performed against you to 2 power stages'
             ' of damage.')

CARD_POWER = CardPowerPhysicalDefense(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
    damage_modifier=DamageModifier(power_max=2))
