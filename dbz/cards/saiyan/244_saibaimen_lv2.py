import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Saibaimen Lv2'
LEVEL = 2
SAGA = 'Saiyan'
CARD_NUMBER = '244'
RARITY = 5
DECK_LIMIT = 3
CHARACTER = 'Saibaimen'
IS_HERO = False
POWER_UP_RATING = 2
POWER_STAGES = range(2000, 3800+1, 200)
CARD_TEXT = ('Reduce the damage from an energy attack performed against you to 2 life cards'
             ' of damage.')

CARD_POWER = CardPowerEnergyDefense(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
    damage_modifier=DamageModifier(life_max=2))
