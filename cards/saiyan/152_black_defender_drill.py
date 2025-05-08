import sys

from card_power_on_damage_modification import CardPowerOnDamageModification
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Black Defender Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '152'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Black'
RESTRICTED = False
CARD_TEXT = ('All energy attacks performed against you do 1 less life card of damage.')

CARD_POWER = CardPowerOnDamageModification(
    NAME, CARD_TEXT, opp_energy=DamageModifier(life_add=-1))
