import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Gohan Lv1 HT'
LEVEL = 1
SAGA = 'Saiyan'
CARD_NUMBER = '181'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Gohan'
IS_HERO = True
POWER_UP_RATING = 1
POWER_STAGES = range(100, 1000+1, 100)
CARD_TEXT = ('Energy Attack. Costs 1 stage and does 3 life card draws of damage.')

CARD_POWER = CardPowerEnergyAttack(
    NAME, CARD_TEXT, exhaust=False, discard=False,
    cost=Cost.energy_attack(power=1),
    damage=Damage.energy_attack(life=3))
