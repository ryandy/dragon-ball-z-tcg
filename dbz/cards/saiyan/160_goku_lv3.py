import sys

from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Goku Lv3'
LEVEL = 3
SAGA = 'Saiyan'
CARD_NUMBER = '160'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Goku'
IS_HERO = True
POWER_UP_RATING = 3
POWER_STAGES = range(8000, 12500+1, 500)
CARD_TEXT = ('Prevent 2 life card draws from being discarded from a successful energy attack.')

CARD_POWER = CardPowerEnergyDefense(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
    damage_modifier=DamageModifier(life_prevent=2))
