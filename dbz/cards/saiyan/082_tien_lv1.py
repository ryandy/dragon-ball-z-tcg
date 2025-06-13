import sys

from dbz.card_power_attack import CardPowerPhysicalAttackMultiForm
from dbz.card_power_defense import CardPowerPhysicalDefense
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Tien Lv1'
LEVEL = 1
SAGA = 'Saiyan'
CARD_NUMBER = '82'
RARITY = 3
DECK_LIMIT = 1
CHARACTER = 'Tien'
IS_HERO = True
POWER_UP_RATING = 1
POWER_STAGES = range(100, 1000+1, 100)
CARD_TEXT = ('Multi-Form allows two physical attacks, one after another, or a defense against a'
             ' physical attack preventing 4 stages of successful damage.')

CARD_POWER = [
    CardPowerPhysicalAttackMultiForm(NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False),
    CardPowerPhysicalDefense(NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
                             damage_modifier=DamageModifier(power_prevent=4))
]
