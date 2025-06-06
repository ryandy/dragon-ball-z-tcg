import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Goku Lv4'
LEVEL = 4
SAGA = 'Saiyan'
CARD_NUMBER = 'P1'
RARITY = 2
DECK_LIMIT = 1
CHARACTER = 'Goku'
IS_HERO = True
POWER_UP_RATING = 4
POWER_STAGES = range(14000, 32000+1, 2000)
CARD_TEXT = ('Spirit bomb energy attack, costs 1 stage to do.')

CARD_POWER = CardPowerEnergyAttack(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
    cost=Cost.energy_attack(power=1))
