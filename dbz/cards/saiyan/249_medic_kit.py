import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Medic Kit'
SAGA = 'Saiyan'
CARD_NUMBER = '249'
RARITY = 6
DECK_LIMIT = 1
CHARACTER = None
STYLE = None
CARD_TEXT = ('Place the top 3 discard cards at the bottom of the Life Deck.')

CARD_POWER = CardPowerNonCombatAttack(NAME, CARD_TEXT, rejuvenate_count=3)
