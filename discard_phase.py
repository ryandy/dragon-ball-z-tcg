import random
import sys

from phase import Phase
from util import dprint


class DiscardPhase(Phase):
    def __init__(self, player, combat_phase):
        self.player = player
        self.combat_phase = combat_phase

    def execute(self):
        if len(self.player.hand) > 1:
            dprint(f'{self.player.name()} must discard down to 1 card')
        while len(self.player.hand) > 1:
            card = self.player.choose_hand_discard_card()
            self.player.discard(card)

        if len(self.player.opponent.hand) > 1:
            dprint(f'{self.player.opponent.name()} must discard down to 1 card')
        while len(self.player.opponent.hand) > 1:
            card = self.player.opponent.choose_hand_discard_card()
            self.player.opponent.discard(card)

        if self.combat_phase.skipped:
            self.player.rejuvenate()
