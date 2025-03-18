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


class Runner:
    def __init__(self, deck1, deck2):
        State.TURN = 0
        self.players = [
            Player(deck1, self),
            Player(deck2, self)]
        #random.shuffle(self.players)

        self.players[0].register_opponent(self.players[1])
        self.players[1].register_opponent(self.players[0])

    def __repr__(self):
        return f'{self.players[0]} vs {self.players[1]}'

    def run(self):
        while True:
            try:
                self.take_turn()
            except GameOver as err:
                print(f'{err.winning_player.name()} has won!')
                print(f'{err}')
                #err.winning_player.show_discard_pile()
                return
            State.TURN += 1

    def take_turn(self):
        print(f'Turn {State.TURN}')

        player = self.players[State.TURN % 2]

        # BEGINNING OF TURN
        
        draw_phase = DrawPhase(player)
        draw_phase.execute()

        non_combat_phase = NonCombatPhase(player)
        non_combat_phase.execute()

        power_up_phase = PowerUpPhase(player)
        power_up_phase.execute()

        combat_phase = CombatPhase(player)
        combat_phase.execute()

        discard_phase = DiscardPhase(player, combat_phase)
        discard_phase.execute()

        # END OF TURN

        #if State.TURN % 2 == 1:
        #    player.show()

        print()
