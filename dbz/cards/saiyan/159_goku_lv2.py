import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Goku Lv2'
LEVEL = 2
SAGA = 'Saiyan'
CARD_NUMBER = '159'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Goku'
IS_HERO = True
POWER_UP_RATING = 2
POWER_STAGES = range(3200, 7700+1, 500)
CARD_TEXT = ('Kaio-Ken Power Level Booster. Physical attack draining 4 power stages, no matter what'
             ' Goku\'s power is. Do not consult table.')

CARD_POWER = CardPowerPhysicalAttack(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
    damage=Damage(power=4))
