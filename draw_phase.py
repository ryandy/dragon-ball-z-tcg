import sys

from card_power_on_draw import CardPowerOnDraw
from combat_card import CombatCard
from phase import Phase


class DrawPhase(Phase):
    def __init__(self, player, is_attacker=None):
        self.player = player
        self.is_attacker = is_attacker
        self.draw_count = 3
        self.discard_pile_draw_count = 0

    def execute(self):
        for player in [self.player, self.player.opponent]:
            draw_powers = player.get_valid_card_powers(CardPowerOnDraw)
            for draw_power in draw_powers:
                draw_power.on_draw(self)

        for _ in range(self.draw_count):
            card = self.player.draw()

        for _ in range(self.discard_pile_draw_count):
            if len(self.player.discard_pile) > 0:
                card = self.player.discard_pile.draw_from_bottom()
                self.player.draw(card=card)
