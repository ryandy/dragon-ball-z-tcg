import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerAnyDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Vegeta\'s Surprise Defense'
SUBTYPE = 'Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '100'
RARITY = 3
DECK_LIMIT = None
CHARACTER = 'Vegeta'
STYLE = None
CARD_TEXT = ('Stop a physical or energy attack. Remove from the game after use.')

CARD_POWER = CardPowerAnyDefense(NAME, CARD_TEXT, remove_from_game=True)
