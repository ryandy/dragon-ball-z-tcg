import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Yamcha\'s Physical Defense'
SUBTYPE = 'Physical Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '116'
RARITY = 3
DECK_LIMIT = None
CHARACTER = 'Yamcha'
STYLE = None
CARD_TEXT = ('Prevents 3 life cards from being taken in a successful physical attack.')

CARD_POWER = CardPowerPhysicalDefense(
    NAME, CARD_TEXT, damage_modifier=DamageModifier(life_prevent=3))
