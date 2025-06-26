import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Goku\'s Attack'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = 'BK1'
RARITY = 2
DECK_LIMIT = None
CHARACTER = 'Goku'
STYLE = None
CARD_TEXT = ('Physical attack doing 5 life cards of damage. Remove from the game after use.')

CARD_POWER = CardPowerPhysicalAttack(
    NAME, CARD_TEXT, remove_from_game=True,
    damage=Damage(life=5))
