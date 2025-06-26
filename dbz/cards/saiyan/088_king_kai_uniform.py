import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'King Kai Uniform'
SAGA = 'Saiyan'
CARD_NUMBER = '88'
RARITY = 3
DECK_LIMIT = 1
CHARACTER = 'King Kai'
STYLE = None
CARD_TEXT = ('Prevents 1 life card discard from any successful physical attack.')

CARD_POWER = CardPowerPhysicalDefense(
    NAME, CARD_TEXT, damage_modifier=DamageModifier(life_prevent=1))
