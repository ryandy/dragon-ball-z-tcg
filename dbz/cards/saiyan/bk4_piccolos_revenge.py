import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Piccolo\'s Revenge'
SUBTYPE = 'Energy Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = 'BK4'
RARITY = 2
DECK_LIMIT = None
CHARACTER = 'Piccolo'
STYLE = None
CARD_TEXT = ('Your successful energy beam attack slashes defender for 6 life cards.'
             ' Remove from the game after use.')

CARD_POWER = CardPowerEnergyAttack(
    NAME, CARD_TEXT, remove_from_game=True,
    damage=Damage(life=6))
