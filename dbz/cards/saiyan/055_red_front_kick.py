import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Red Front Kick'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '55'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Red'
CARD_TEXT = ('Physical attack doing +1 stage of damage if successful. Raise card user\'s'
             ' anger level 1.')

CARD_POWER = CardPowerPhysicalAttack(
    NAME, CARD_TEXT, own_anger=1, damage_modifier=DamageModifier(power_add=1))
