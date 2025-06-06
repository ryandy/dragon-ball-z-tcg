import sys

from dbz.card_power_attack import CardPowerPhysicalAttack, CardPowerEnergyAttack
from dbz.card_power_defense import CardPowerPhysicalDefense, CardPowerEnergyDefense
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Yajirobe Lv1'
LEVEL = 1
SAGA = 'Saiyan'
CARD_NUMBER = '106'
RARITY = 3
DECK_LIMIT = 1
CHARACTER = 'Yajirobe'
IS_HERO = True
POWER_UP_RATING = 1
POWER_STAGES = range(100, 1000+1, 100)
CARD_TEXT = ('Physical Attack.')

CARD_POWER = CardPowerPhysicalAttack(NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False)
