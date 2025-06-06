import sys

from dbz.phase import Phase
from dbz.state import State


class NonCombatPhase(Phase):
    def __init__(self, player):
        self.player = player

    def execute(self):
        State.PHASE = self

        card = self.player.choose_hand_non_combat_card()
        while card:
            self.player.play_non_combat_card(card)
            card = self.player.choose_hand_non_combat_card()
