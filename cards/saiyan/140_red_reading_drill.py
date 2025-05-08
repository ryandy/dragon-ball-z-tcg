import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerAnyDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Red Reading Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '140'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Red'
RESTRICTED = False
CARD_TEXT = ('Once per Combat, you may prevent 1 life card of damage from any attack.')

CARD_POWER = CardPowerAnyDefense(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
    damage_modifier=DamageModifier(life_prevent=1))
