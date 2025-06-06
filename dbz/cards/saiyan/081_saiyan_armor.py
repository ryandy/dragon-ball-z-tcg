import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Saiyan Armor'
SAGA = 'Saiyan'
CARD_NUMBER = '81'
RARITY = 3
DECK_LIMIT = 1
CHARACTER = None
STYLE = 'Saiyan'
CARD_TEXT = ('Prevents 1 life card dicard from any successful energy attack.')

CARD_POWER = CardPowerEnergyDefense(
    NAME, CARD_TEXT, damage_modifier=DamageModifier(life_prevent=1))
