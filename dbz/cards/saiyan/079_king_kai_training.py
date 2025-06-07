import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'King Kai Training'
SAGA = 'Saiyan'
CARD_NUMBER = '79'
RARITY = 3
DECK_LIMIT = None
CHARACTER = 'King Kai'
STYLE = None
CARD_TEXT = ('Heroes only. Choose 2 cards from your discard pile and place them on'
             ' the bottom of your Life Deck.')

CARD_POWER = CardPowerNonCombatAttack(NAME, CARD_TEXT, rejuvenate_choice_count=2, heroes_only=True)
