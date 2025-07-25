import sys

from dbz.card_power_on_draw import CardPowerOnDraw
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Raditz Honor Duel!'
SAGA = 'Saiyan'
CARD_NUMBER = '102'
RARITY = 3
DECK_LIMIT = None
CHARACTER = 'Raditz'
STYLE = None
CARD_TEXT = (
    'Use when entering Combat as the defender. Instead of drawing 3 cards from your life deck,'
    ' draw the bottom 3 cards from your discard pile. Remove from the game after use.')


class CardPowerOnDrawRHD(CardPowerOnDraw):
    def on_effect(self, phase):
        # If this is played twice in one turn, you shouldn't end up drawing 6 cards
        super().on_effect(phase)
        if phase.draw_count < 0:
            phase.discard_pile_bottom_draw_count -= abs(phase.draw_count)
            phase.draw_count = 0


CARD_POWER = CardPowerOnDrawRHD(
    NAME, CARD_TEXT, own_defend_draw_add=-3, own_defend_draw_from_discard_bottom_add=3,
    choice=True, remove_from_game=True)
