import sys

from dragon_ball_card import DragonBallCard
from phase import Phase


class NonCombatPhase(Phase):
    def __init__(self, player):
        self.player = player

    def execute(self):
        card = self.player.play_non_combat_card()
        while card:
            if isinstance(card, DragonBallCard):
                for card_power in card.card_powers:
                    card_power.on_play(self.player, self)
            card = self.player.play_non_combat_card()
