import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Blazing Anger!'
SAGA = 'Saiyan'
CARD_NUMBER = '99'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Increase your anger level by 2. Take the top 2 cards from your discard pile and'
             ' place them at the bottom of your life deck.')

CARD_POWER = CardPowerNonCombatAttack(NAME, CARD_TEXT, own_anger=2, rejuvenate_count=2)
