import sys

from card_power_on_damage_modification import CardPowerOnDamageModification
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Chiaotzu\'s Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '230'
RARITY = 5
DECK_LIMIT = None
CHARACTER = 'Chiaotzu'
STYLE = None
RESTRICTED = False
CARD_TEXT = ('All physical attacks performed against you do 1 less power stage of damage.')

CARD_POWER = CardPowerOnDamageModification(
    NAME, CARD_TEXT, opp_physical=DamageModifier(power_add=-1))
