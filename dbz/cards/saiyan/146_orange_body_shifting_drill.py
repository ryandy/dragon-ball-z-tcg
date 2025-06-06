import sys

from dbz.card_power_on_cost_modification import CardPowerOnCostModification
from dbz.character import Character
from dbz.cost import Cost
from dbz.cost_modifier import CostModifier


TYPE = 'Drill'
NAME = 'Orange Body Shifting Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '146'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Orange'
RESTRICTED = False
CARD_TEXT = ('All of your energy attacks that cost 2 power stages to perform now only cost'
             ' 1 power stage to perform.')

CARD_POWER = CardPowerOnCostModification(
    NAME, CARD_TEXT, own_energy=CostModifier(power_ittt={2:1}))
