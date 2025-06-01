import sys

from card_power_defense_shield import CardPowerAnyDefenseShield
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'T-Rex Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '226'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Defense Shield: When defending in Combat, stop the first unstopped attack'
             ' performed on you. Remove from the game after use.')

CARD_POWER = CardPowerAnyDefenseShield(NAME, CARD_TEXT, remove_from_game=True)
