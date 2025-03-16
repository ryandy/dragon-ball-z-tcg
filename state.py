import sys

from combat_phase import CombatPhase
from discard_phase import DiscardPhase
from draw_phase import DrawPhase
from exception import GameOver
from non_combat_phase import NonCombatPhase
from player import Player
from power_up_phase import PowerUpPhase


class State:
    def __init__(self, deck1, deck2):
        self.turn = 0
        self.players = [
            Player(deck1),
            Player(deck2)]

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
                #print()
                #err.player.opponent.show()
                return
            self.turn += 1

    def take_turn(self):
        print(f'Turn {self.turn}')

        player = self.players[self.turn % 2]

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

        #if self.turn % 2 == 1:
        #    player.show()

        print()
