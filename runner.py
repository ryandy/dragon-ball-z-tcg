import random
import sys

from combat_phase import CombatPhase
from discard_phase import DiscardPhase
from draw_phase import DrawPhase
from exception import GameOver
from non_combat_phase import NonCombatPhase
from player import Player
from power_up_phase import PowerUpPhase
from state import State
from util import dprint


class Runner:
    def __init__(self, deck1, deck2):
        State.TURN = 0
        State.COMBAT_ROUND = 0

        self.players = [
            Player(deck1, self),
            Player(deck2, self)]
        #random.shuffle(self.players)

        # Disambiguate player names
        if self.players[0].name == self.players[1].name:
            self.players[0].name = f'{self.players[0].name}-1'
            self.players[1].name = f'{self.players[1].name}-2'

        self.players[0].register_opponent(self.players[1])
        self.players[1].register_opponent(self.players[0])

    def __repr__(self):
        return f'{self.players[0].name} vs {self.players[1].name}'

    def run(self):
        while True:
            State.COMBAT_ROUND = 0
            try:
                self.take_turn()
            except GameOver as err:
                dprint(f'{err.winning_player.name} wins!')
                dprint(f'{err}')
                return
            State.TURN += 1

    def beginning_of_turn(self):
        attacker = self.players[State.TURN % 2]
        for player in [attacker, attacker.opponent]:
            player.exhaust_expired_card_powers()
        for player in self.players:
            player.show_summary()
        attacker.check_for_dragon_ball_victory()

    def end_of_turn(self):
        pass

    def take_turn(self):
        player = self.players[State.TURN % 2]
        header = f'========== Turn {State.TURN+1}: {player} =========='
        border = '=' * len(header)
        dprint(border)
        dprint(header)
        dprint(border)

        self.beginning_of_turn()

        draw_phase = DrawPhase(player)
        draw_phase.execute()

        non_combat_phase = NonCombatPhase(player)
        non_combat_phase.execute()

        power_up_phase = PowerUpPhase(player)
        power_up_phase.execute()

        combat_phase = CombatPhase(player, self.players)
        combat_phase.execute()

        discard_phase = DiscardPhase(player, combat_phase)
        discard_phase.execute()

        self.end_of_turn()

        dprint()
