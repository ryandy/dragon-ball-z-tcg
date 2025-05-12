import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Raditz Lv2'
LEVEL = 2
SAGA = 'Saiyan'
CARD_NUMBER = '171'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Raditz'
IS_HERO = False
POWER_UP_RATING = 2
POWER_STAGES = range(2000, 3800+1, 200)
CARD_TEXT = ('Saiyan Energy Blast does 3 life card draw of damage and costs only 1 power stage'
             ' to perform.')

CARD_POWER = CardPowerEnergyAttack(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
    cost=Cost.energy_attack(power=1),
    damage=Damage.energy_attack(life=3))
