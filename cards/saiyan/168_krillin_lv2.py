import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Krillin Lv2'
LEVEL = 2
SAGA = 'Saiyan'
CARD_NUMBER = '168'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Krillin'
IS_HERO = True
POWER_UP_RATING = 2
POWER_STAGES = range(500, 1400+1, 100)
CARD_TEXT = ('Destructo-Disk Energy Attack doing 3 life card draws of damage.')

CARD_POWER = CardPowerEnergyAttack(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
    damage=Damage.energy_attack(life=3))
