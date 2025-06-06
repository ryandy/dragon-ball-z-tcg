import sys

from card_power_defense import CardPowerEnergyDefense, CardPowerAnyDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'The Tail Grows Back'
SUBTYPE = 'Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '201'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Increase a personality\'s power stage to its maximum level.'
             ' Remove from the game after use.')

CARD_POWER = CardPowerAnyDefense(
    NAME, CARD_TEXT, any_power=10, remove_from_game=True,
    damage_modifier=DamageModifier.none())
