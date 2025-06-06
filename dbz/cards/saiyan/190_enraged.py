import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Enraged!'
SAGA = 'Saiyan'
CARD_NUMBER = '190'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Increase your anger level by 2. Select 2 cards from your discard pile and place'
             ' them at the bottom of your Life Deck. Remove from the game after use.')

CARD_POWER = CardPowerNonCombatAttack(
    NAME, CARD_TEXT, own_anger=2, rejuvenate_choice_count=2, remove_from_game=True)
