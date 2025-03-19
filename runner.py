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
        State.COMBAT_ROUND = 0

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
            State.COMBAT_ROUND = 0
            try:
                self.take_turn()
            except GameOver as err:
                print(f'{err.winning_player.name()} has won!')
                print(f'{err}')
                #err.winning_player.show_discard_pile()
                return
            State.TURN += 1

    def beginning_of_turn(self):
        for idx in range(State.TURN, State.TURN + 2):
            self.players[idx%2].exhaust_expired_card_powers()

    def end_of_turn(self):
        pass

    def take_turn(self):
        print(f'==== Turn {State.TURN} ====')

        self.beginning_of_turn()

        #for player in self.players:
        #    print(f'{player.name()}\'s start-of-turn energy defense powers:')
        #    for card_power in player.card_powers:
        #        if isinstance(card_power, CardPowerEnergyDefense):
        #            print(f'  {card_power.name}, {card_power.card}, {card_power.is_exhausted()}')
        #    print(f'{player.name()}\'s start-of-turn hand:')
        #    for card in player.hand:
        #        print(f'  {card.name}')
        #print()

        player = self.players[State.TURN % 2]

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

        self.end_of_turn()

        print()
