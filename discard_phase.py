import random
import sys

from phase import Phase
from state import State
from util import dprint


class DiscardPhase(Phase):
    def __init__(self, player, combat_phase):
        self.player = player
        self.combat_phase = combat_phase

    def execute(self):
        State.PHASE = self

        for player in State.gen_players():
            if len(player.hand) > 1:
                dprint(f'{player} must discard down to 1 card')
            while len(player.hand) > 1:
                card = player.choose_hand_discard_card()
                player.discard(card)

        if self.combat_phase.skipped:
            self.player.rejuvenate()
