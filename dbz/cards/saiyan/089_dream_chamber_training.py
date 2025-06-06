import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Dream Chamber Training'
SAGA = 'Saiyan'
CARD_NUMBER = '89'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Heroes only. Choose 2 cards from your discard pile and place them on'
             ' the bottom of your Life Deck. Remove from the game after use.')

CARD_POWER = CardPowerNonCombatAttack(
    NAME, CARD_TEXT, rejuvenate_choice_count=2, heroes_only=True, remove_from_game=True)
