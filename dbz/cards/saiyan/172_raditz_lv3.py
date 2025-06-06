import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Raditz Lv3'
LEVEL = 3
SAGA = 'Saiyan'
CARD_NUMBER = '170'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Raditz'
IS_HERO = False
POWER_UP_RATING = 1
POWER_STAGES = range(1100, 2000+1, 100)
CARD_TEXT = ('Reduce the damage from an energy attack performed against you to 2 life cards'
             ' of damage, or Saiyan Energy Blast which does 3 life card draw of damage and'
             ' costs only 1 power stage to perform.')

CARD_POWER = [
    CardPowerEnergyDefense(
        NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
        damage_modifier=DamageModifier(life_max=2)),    
    CardPowerEnergyAttack(
        NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
        cost=Cost.energy_attack(power=1),
        damage=Damage.energy_attack(life=3))
]
