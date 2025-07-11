import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Vegeta HT Lv1'
LEVEL = 1
SAGA = 'Saiyan'
CARD_NUMBER = '184'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Vegeta'
IS_HERO = False
POWER_UP_RATING = 1
POWER_STAGES = range(2000, 3800+1, 200)
CARD_TEXT = ('Stop an energy attack.')

CARD_POWER = CardPowerEnergyDefense(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False)
