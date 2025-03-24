import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Bulma Lv1'
LEVEL = 1
SAGA = 'Saiyan'
CARD_NUMBER = '87'
RARITY = 3
DECK_LIMIT = 1
CHARACTER = 'Bulma'
IS_HERO = True
POWER_UP_RATING = 1
POWER_STAGES = range(100, 1000+1, 100)
CARD_TEXT = ('Scientific Defense. Reduces the damage done by an energy attack by 2 life'
             ' card draws.')


CARD_POWER = CardPowerEnergyDefense(
    NAME, CARD_TEXT, exhaust=False, discard=False,
    damage_modifier=DamageModifier(life_prevent=2))
