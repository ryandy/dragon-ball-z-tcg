import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Saibaimen Lv1'
LEVEL = 1
SAGA = 'Saiyan'
CARD_NUMBER = '243'
RARITY = 5
DECK_LIMIT = 3
CHARACTER = 'Saibaimen'
IS_HERO = False
POWER_UP_RATING = 1
POWER_STAGES = range(1100, 2000+1, 100)
CARD_TEXT = ('Reduce the damage from an energy attack performed against you to 2 life cards'
             ' of damage.')

CARD_POWER = CardPowerEnergyDefense(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
    damage_modifier=DamageModifier(life_max=2))
