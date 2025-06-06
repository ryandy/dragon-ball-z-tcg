import sys

from dbz.card_power_defense_shield import CardPowerPhysicalDefenseShield
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Fall 7 times, get up 8 times.'
SAGA = 'Saiyan'
CARD_NUMBER = '30'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Defense Shield: Stop the first unstopped physical attack performed against you.'
             ' Remove from the game after use.')

CARD_POWER = CardPowerPhysicalDefenseShield(NAME, CARD_TEXT, remove_from_game=True)
