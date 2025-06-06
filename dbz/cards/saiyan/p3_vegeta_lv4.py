import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerNonCombatAttack
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Vegeta Lv4'
LEVEL = 4
SAGA = 'Saiyan'
CARD_NUMBER = 'P3'
RARITY = 2
DECK_LIMIT = 1
CHARACTER = 'Vegeta'
IS_HERO = False
POWER_UP_RATING = 4
POWER_STAGES = range(20000, 38000+1, 2000)
CARD_TEXT = ('Vegeta\'s laugh reduces a foe\'s Main Personality\'s power rating by 3.')

CARD_POWER = CardPowerNonCombatAttack(
    NAME, CARD_TEXT, opp_power=-3, exhaust_until_next_turn=True, discard=False)
