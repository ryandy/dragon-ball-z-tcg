import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerNonCombatAttack
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Krillin Lv3'
LEVEL = 3
SAGA = 'Saiyan'
CARD_NUMBER = '169'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Krillin'
IS_HERO = True
POWER_UP_RATING = 3
POWER_STAGES = list(range(1500, 3100+1, 200)) + [3200]
CARD_TEXT = ('Take 1 card from the discard pile and place it at the bottom of your Life Deck.')

CARD_POWER = CardPowerNonCombatAttack(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False, rejuvenate_choice_count=1)
