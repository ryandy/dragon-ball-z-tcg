import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Blue Shoulder Wheel'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '14'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Blue'
CARD_TEXT = ('Physical Attack doing +1 stage of damage if successful. Raises your anger level by 1'
             ' and lowers foe\'s anger level by 1.')


CARD_POWER = CardPowerPhysicalAttack(
    NAME, CARD_TEXT, damage_modifier=DamageModifier(power_add=1), own_anger=1, opp_anger=-1)
