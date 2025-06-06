import sys

from card_power_on_damage_modification import CardPowerOnDamageModification
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Blue Life Defense Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '233'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Blue'
RESTRICTED = False
CARD_TEXT = ('Prevent 1 life card of damage from being taken whenever a successful attack'
             ' happens on the card owner.')

CARD_POWER = CardPowerOnDamageModification(
    NAME, CARD_TEXT,
    opp_physical=DamageModifier(life_prevent=1),
    opp_energy=DamageModifier(life_prevent=1))
