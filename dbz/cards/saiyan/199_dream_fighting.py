import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Dream Fighting'
SUBTYPE = 'Combat - Attack'  # Must be used as an attack according to 11/24/04 CRD pg3
SAGA = 'Saiyan'
CARD_NUMBER = '199'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('End Combat. Place the bottom card of your discard pile at the bottom'
             ' of your Life Deck. Remove from the game after use.')

# Assuming it also effectively stops the attack
CARD_POWER = CardPowerNonCombatAttack(
    NAME, CARD_TEXT, force_end_combat=True, rejuvenate_bottom_count=1, remove_from_game=True)
