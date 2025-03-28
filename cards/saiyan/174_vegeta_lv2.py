import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Vegeta Lv2'
LEVEL = 2
SAGA = 'Saiyan'
CARD_NUMBER = '174'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Vegeta'
IS_HERO = False
POWER_UP_RATING = 4
POWER_STAGES = range(4200, 8700+1, 500)
CARD_TEXT = ('Saiyan Energy Blast does 3 life card draw of damage and only costs 1 power stage'
             ' to perform.')

CARD_POWER = CardPowerEnergyAttack(
    NAME, CARD_TEXT, exhaust=False, discard=False,
    cost=Cost.energy_attack(power=1),
    damage=Damage.energy_attack(life=3))
