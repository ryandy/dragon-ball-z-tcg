import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Respect the Spirit'
SAGA = 'Saiyan'
CARD_NUMBER = '193'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Place 2 discarded cards at the bottom of your Life Deck. Remove from the game'
             ' after use.')

CARD_POWER = CardPowerNonCombatAttack(
    NAME, CARD_TEXT, rejuvenate_choice_count=2, remove_from_game=True)
