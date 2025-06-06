import sys

from dbz.card_power_on_damage_modification import CardPowerOnDamageModification
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Orange Tripping Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '130'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Orange'
RESTRICTED = False
CARD_TEXT = ('All energy attacks performed against you do 1 less life card of damage.')

CARD_POWER = CardPowerOnDamageModification(
    NAME, CARD_TEXT, opp_energy=DamageModifier(life_add=-1))
