import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Saiyan Armor'
SAGA = 'Saiyan'
CARD_NUMBER = '88'
RARITY = 3
DECK_LIMIT = 1
CHARACTER = None
STYLE = None
CARD_TEXT = ('Prevents 1 life card dicard from any successful physical attack.')

CARD_POWER = CardPowerPhysicalDefense(
    NAME, CARD_TEXT, damage_modifier=DamageModifier(life_prevent=1))
