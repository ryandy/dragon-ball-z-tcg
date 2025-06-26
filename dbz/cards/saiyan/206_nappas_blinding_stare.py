import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Nappa\'s Blinding Stare'
SUBTYPE = 'Combat - Attack'  # Must be used as an attack according to 11/24/04 CRD pg3
SAGA = 'Saiyan'
CARD_NUMBER = '206'
RARITY = 5
DECK_LIMIT = None
CHARACTER = 'Nappa'
STYLE = None
CARD_TEXT = ('End Combat. Remove from the game after use.')

CARD_POWER = CardPowerNonCombatAttack(
    NAME, CARD_TEXT, force_end_combat=True, remove_from_game=True)
