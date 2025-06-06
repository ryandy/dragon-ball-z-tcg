import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerNonCombatAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerAnyDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Grabbing the Tail'
SUBTYPE = 'Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '205'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Reduce the foe\'s power level by 4 stages. Remove from the game after use.')

CARD_POWER = CardPowerNonCombatAttack(NAME, CARD_TEXT, opp_power=-4, remove_from_game=True)
