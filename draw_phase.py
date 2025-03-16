import sys

from combat_card import CombatCard
from phase import Phase


class DrawPhase(Phase):
    def __init__(self, player, is_defender=False):
        self.player = player
        self.is_defender = is_defender

    def execute(self):
        if not self.is_defender:
            # "BEGINNING OF TURN" (attacker before defender)
            pass

        # TODO: if an unplayable drill is drawn, it can be shuffled back into the deck
        for _ in range(3):
            self.player.draw()

        # Register callbacks for all combat cards in hand
        for card in self.player.hand:
            if isinstance(card, CombatCard):
                for timing, (cost, damage, execute) in card.card_power.items():
                    self.player.register_power(timing, card, cost, damage, execute)
