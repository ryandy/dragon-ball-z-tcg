import sys

from card_power_defense_shield import CardPowerAnyDefenseShield
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'It\'s the Little Things That Matter'
SAGA = 'Saiyan'
CARD_NUMBER = '33'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Defense Shield: Stop the first unstopped energy or physical attack performed'
             ' against you. Remove from the game after use.')

CARD_POWER = CardPowerAnyDefenseShield(NAME, CARD_TEXT, remove_from_game=True)
