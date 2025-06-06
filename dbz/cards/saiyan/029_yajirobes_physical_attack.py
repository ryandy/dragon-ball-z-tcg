import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Yajirobe\'s Physical Attack'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '29'
RARITY = 1
DECK_LIMIT = None
CHARACTER = 'Yajirobe'
STYLE = None
CARD_TEXT = ('Physical attack doing 2 draws from the life deck if not stopped. Remove from the'
             ' game after use.')

CARD_POWER = CardPowerPhysicalAttack(NAME, CARD_TEXT, damage=Damage(life=2), remove_from_game=True)
