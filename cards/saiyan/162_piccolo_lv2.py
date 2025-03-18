import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Piccolo Lv2'
LEVEL = 2
SAGA = 'Saiyan'
CARD_NUMBER = '162'
RARITY = 4
CHARACTER = 'Piccolo'
IS_HERO = True
POWER_UP_RATING = 2
POWER_STAGES = list(range(1500, 3100+1, 200)) + [3200]
CARD_TEXT = ('Special Energy Beam Cannon. This energy blast only takes 1 power stage to use and'
             ' does 2 life card draws of damage.')

CARD_POWER = CardPowerEnergyAttack(
    NAME, CARD_TEXT, exhaust=False, discard=False,
    cost=Cost.energy_attack(power=1),
    damage=Damage.energy_attack(life=2))
