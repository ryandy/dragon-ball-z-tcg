import itertools
import random
import sys

import tabulate

from dbz.card_power_on_end_of_turn import CardPowerOnEndOfTurn
from dbz.card_power_on_entering_turn import CardPowerOnEnteringTurn
from dbz.combat_phase import CombatPhase
from dbz.discard_phase import DiscardPhase
from dbz.draw_phase import DrawPhase
from dbz.exception import DeckEmpty, GameOver
from dbz.non_combat_phase import NonCombatPhase
from dbz.player import Player
from dbz.power_up_phase import PowerUpPhase
from dbz.state import State
from dbz.util import dprint


class Runner:
    def __init__(self, deck1, deck2):
        State.TURN = 0
        State.COMBAT_ROUND = 0

        self.players = [
            Player(deck=deck1, interactive=State.INTERACTIVE),
            Player(deck=deck2)]
        #random.shuffle(self.players)

        # Disambiguate player names
        if self.players[0].name == self.players[1].name:
            self.players[0].name = f'{self.players[0].name}-1'
            self.players[1].name = f'{self.players[1].name}-2'

        self.players[0].register_opponent(self.players[1])
        self.players[1].register_opponent(self.players[0])

    def __repr__(self):
        return f'{self.players[0].name} vs {self.players[1].name}'

    def show_summary(self):
        tabulate.PRESERVE_WHITESPACE = True
        summaries = [player.get_summary() for player in reversed(self.players)]
        table = tabulate.tabulate(
            itertools.zip_longest(*reversed(summaries)),
            tablefmt='fancy_grid')
        dprint(table)

    def run(self):
        while True:
            State.COMBAT_ROUND = 0

            try:
                self.take_turn()

            except GameOver as err:
                dprint(f'{err.winning_player} wins!')
                dprint(f'{err}')
                return

            except DeckEmpty as err:
                for player in self.players:
                    if len(player.life_deck) == 0:
                        dprint(f'{player.opponent} wins!')
                        dprint(f'{player}\'s Life Deck is empty')
                        return
                assert False

            State.TURN += 1

    def beginning_of_turn(self):
        for player in State.gen_players():
            player.exhaust_expired_card_powers()
        self.show_summary()

        State.TURN_PLAYER.check_for_dragon_ball_victory()

        for player in State.gen_players():
            card_powers = player.get_valid_card_powers(CardPowerOnEnteringTurn)
            for card_power in card_powers:
                card_power.on_entering_turn()

    def end_of_turn(self):
        for player in State.gen_players():
            card_powers = player.get_valid_card_powers(CardPowerOnEndOfTurn)
            for card_power in card_powers:
                card_power.on_end_of_turn()

    def take_turn(self):
        player = self.players[State.TURN % 2]
        State.TURN_PLAYER = player

        header = f'========== Turn {State.TURN+1}: {player} =========='
        border = '=' * len(header)
        dprint(border)
        dprint(header)
        dprint(border)

        self.beginning_of_turn()

        draw_phase = DrawPhase(player, is_attacker=True)
        draw_phase.execute()

        non_combat_phase = NonCombatPhase(player)
        non_combat_phase.execute()

        power_up_phase = PowerUpPhase(player)
        power_up_phase.execute()

        # Refresh summary before player has to decide whether to declare combat
        self.show_summary()

        combat_phase = CombatPhase(self, player, power_up_phase)
        combat_phase.execute()

        discard_phase = DiscardPhase(player, combat_phase)
        discard_phase.execute()

        self.end_of_turn()

        dprint()
