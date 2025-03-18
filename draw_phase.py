import sys

from combat_card import CombatCard
from phase import Phase


class DrawPhase(Phase):
    def __init__(self, player):
        self.player = player

    def execute(self):
        # TODO: if an unplayable drill is drawn, it can be shuffled back into the deck
        for _ in range(3):
            card = self.player.draw()

            # Register callbacks for all new combat cards in hand
            if isinstance(card, CombatCard):
                for card_power in card.card_powers:
                    self.player.register_card_power(card_power)
