import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Raditz Lv4'
LEVEL = 4
SAGA = 'Saiyan'
CARD_NUMBER = 'P4'
RARITY = 2
DECK_LIMIT = 1
CHARACTER = 'Raditz'
IS_HERO = False
POWER_UP_RATING = 4
POWER_STAGES = range(9000, 18000+1, 1000)
CARD_TEXT = ('Saiyan Throat Strike does five stages of physical damage.')

CARD_POWER = CardPowerPhysicalAttack(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
    damage=Damage(power=5))
