import sys

from card_power_on_damage_modification import CardPowerOnDamageModification
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Orange Energy Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '142'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Orange'
RESTRICTED = 'Orange'
CARD_TEXT = ('All energy attacks performed against you do 1 less life card of damage. Can\'t be'
             ' used with any other Orange drills in play.')

CARD_POWER = CardPowerOnDamageModification(
    NAME, CARD_TEXT, opp_energy=DamageModifier(life_add=-1))
