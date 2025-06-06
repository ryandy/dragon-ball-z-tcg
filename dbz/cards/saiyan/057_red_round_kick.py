import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Red Round Kick'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '57'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Red'
CARD_TEXT = ('Physical attack doing +3 stages of damage if successful. Foe\'s anger level'
             ' decreases by 1.')

CARD_POWER = CardPowerPhysicalAttack(
    NAME, CARD_TEXT, opp_anger=-1, damage_modifier=DamageModifier(power_add=3))
