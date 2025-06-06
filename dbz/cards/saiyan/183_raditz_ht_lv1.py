import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerNonCombatAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Raditz HT Lv1'
LEVEL = 1
SAGA = 'Saiyan'
CARD_NUMBER = '183'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Raditz'
IS_HERO = False
POWER_UP_RATING = 1
POWER_STAGES = range(1100, 2000+1, 100)
CARD_TEXT = ('Raise Raditz\'s anger level 1.')

CARD_POWER = CardPowerNonCombatAttack(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
    own_anger=1)
