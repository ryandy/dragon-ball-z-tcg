import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Power Up!'
SAGA = 'Saiyan'
CARD_NUMBER = '22'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Powers up to the personality\'s highest stage. Select 2 discarded cards and place'
             ' them at the bottom of your life deck.')

CARD_POWER = CardPowerNonCombatAttack(NAME, CARD_TEXT, any_power=10, rejuvenate_choice_count=2)
