import sys

from card_power_attack import CardPowerNonCombatAttack
from card_power_on_draw import CardPowerOnDraw
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Goku Honor Duel!'
SAGA = 'Saiyan'
CARD_NUMBER = '101'
RARITY = 3
DECK_LIMIT = None
CHARACTER = 'Goku'
STYLE = None
CARD_TEXT = (
    'Use when entering Combat as the defender. Instead of drawing 3 cards from your life deck,'
    ' draw the bottom 3 cards from your discard pile. Remove from the game after use.')


class CardPowerGHD(CardPowerOnDraw):
    def on_effect(self, phase):
        # If this is played twice in one turn, you shouldn't end up drawing 6 cards
        draws_shifted = max(0, min(3, phase.draw_count))
        phase.discard_pile_draw_count += draw_shifted
        phase.draw_count -= draws_shifted


CARD_POWER = CardPowerGHD(
    NAME, CARD_TEXT, choice=True, remove_from_game=True)
