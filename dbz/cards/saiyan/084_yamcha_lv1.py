import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Yamcha Lv1'
LEVEL = 1
SAGA = 'Saiyan'
CARD_NUMBER = '84'
RARITY = 3
DECK_LIMIT = 1
CHARACTER = 'Yamcha'
IS_HERO = True
POWER_UP_RATING = 1
POWER_STAGES = range(100, 1000+1, 100)
CARD_TEXT = ('Spirit Ball Energy Attack does 2 life card draws of damage.')

CARD_POWER = CardPowerEnergyAttack(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
    damage=Damage.energy_attack(life=2))
