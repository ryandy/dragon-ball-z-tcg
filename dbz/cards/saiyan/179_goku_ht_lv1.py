import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Goku HT Lv1'
LEVEL = 1
SAGA = 'Saiyan'
CARD_NUMBER = '179'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Goku'
IS_HERO = True
POWER_UP_RATING = 1
POWER_STAGES = range(500, 1400+1, 100)
CARD_TEXT = ('Physical Attack. Do not consult the chart and do 4 stages of damage to the foe.')

CARD_POWER = CardPowerPhysicalAttack(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
    damage=Damage(power=4))
