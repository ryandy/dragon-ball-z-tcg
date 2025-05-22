import random
import sys

from card_power_on_discard import CardPowerOnDiscard
from phase import Phase
from state import State
from util import dprint


class DiscardPhase(Phase):
    def __init__(self, player, combat_phase):
        self.player = player
        self.combat_phase = combat_phase
        self.skip_discard = {p:False for p in State.gen_players()}

    def execute(self):
        State.PHASE = self

        for player in State.gen_players():
            card_powers = player.get_valid_card_powers(CardPowerOnDiscard)
            for card_power in card_powers:
                card_power.on_discard(self)

            if self.skip_discard[player]:
                dprint(f'{player} skips the discard phase')
            else:
                if len(player.hand) > 1:
                    dprint(f'{player} must discard down to 1 card')
                while len(player.hand) > 1:
                    card = player.choose_hand_discard_card()
                    player.discard(card)

        if self.combat_phase.skipped:
            self.player.rejuvenate()
