import sys

from dbz.card_power_attack import CardPowerPhysicalAttack, CardPowerEnergyAttack
from dbz.card_power_defense import CardPowerPhysicalDefense, CardPowerEnergyDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier
from dbz.state import State


TYPE = 'Personality'
NAME = 'Gohan Lv3'
LEVEL = 3
SAGA = 'Saiyan'
CARD_NUMBER = '166'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Gohan'
IS_HERO = True
POWER_UP_RATING = 3
POWER_STAGES = list(range(1500, 3100+1, 200)) + [3200]
CARD_TEXT = ('Kamehameha Energy Attack does 3 life card draws and only costs 1 power stage'
             ' to perform.')

CARD_POWER = CardPowerEnergyAttack(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
    cost=Cost.energy_attack(power=1),
    damage=Damage.energy_attack(life=3))
