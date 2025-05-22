import sys

from card_power_defense import CardPowerEnergyDefense, CardPowerAnyDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Dream Fighting'
SUBTYPE = 'Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '199'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('End Combat. Place the bottom card of your discard pile at the bottom'
             ' of your Life Deck. Remove from the game after use.')

# Assuming it also effectively stops the attack
CARD_POWER = CardPowerAnyDefense(
    NAME, CARD_TEXT, force_end_combat=True, rejuvenate_bottom_count=1, remove_from_game=True)
