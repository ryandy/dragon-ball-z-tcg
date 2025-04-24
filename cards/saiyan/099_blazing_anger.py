import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


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
