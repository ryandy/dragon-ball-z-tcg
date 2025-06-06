import sys

from card_power_attack import CardPowerPhysicalAttack, CardPowerEnergyAttack
from card_power_defense import CardPowerPhysicalDefense, CardPowerEnergyDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Yajirobe Lv2'
LEVEL = 2
SAGA = 'Saiyan'
CARD_NUMBER = '107'
RARITY = 3
DECK_LIMIT = 1
CHARACTER = 'Yajirobe'
IS_HERO = True
POWER_UP_RATING = 2
POWER_STAGES = range(500, 1400+1, 100)
CARD_TEXT = ('Energy attack needs 3 power stages to perform.')

CARD_POWER = CardPowerEnergyAttack(NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
                                   cost=Cost.energy_attack(power=3))
