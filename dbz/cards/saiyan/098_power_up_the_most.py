import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Power Up the Most!'
SAGA = 'Saiyan'
CARD_NUMBER = '98'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Powers up to the personality\'s highest stage. Select 2 discarded cards and place'
             ' them at the bottom of your life deck.')

CARD_POWER = CardPowerNonCombatAttack(NAME, CARD_TEXT, any_power=10, rejuvenate_choice_count=2)
