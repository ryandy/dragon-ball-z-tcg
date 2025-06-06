import sys

from dbz.card_power_on_draw import CardPowerOnDraw
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Hero Advantage'
SAGA = 'Saiyan'
CARD_NUMBER = '195'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Heroes only. Use when entering Combat as the defender. Instead of drawing 3 cards'
             ' from your life deck, draw the top 3 cards from your discard pile. If there are not'
             ' enough cards in the discard pile, this card cannot be used.'
             ' Remove from the game after use.')


class CardPowerOnDrawHA(CardPowerOnDraw):
    def on_condition(self, phase):
        return (self.player.control_personality.is_hero
                and len(self.player.discard_pile) >= 3)

    def on_effect(self, phase):
        # If this is played twice in one turn, you shouldn't end up drawing 6 cards
        super().on_effect(phase)
        if phase.draw_count < 0:
            phase.discard_pile_draw_count -= abs(phase.draw_count)
            phase.draw_count = 0


CARD_POWER = CardPowerOnDrawHA(
    NAME, CARD_TEXT, own_defend_draw_add=-3, own_defend_draw_from_discard_add=3,
    choice=True, remove_from_game=True)
