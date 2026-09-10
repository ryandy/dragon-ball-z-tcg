import itertools
import random
import sys

from dbz.card_power import CardPower
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
from dbz.util import dprint, dprint_table


class Runner:
    def __init__(self, deck1, deck2):
        State.TURN = 0
        State.COMBAT_ROUND = 0

        self.players = [
            Player(deck=deck1, player_num=1, interactive=State.INTERACTIVE),
            Player(deck=deck2, player_num=2)]

        # Check the D Power Rule
        power1 = self.players[0].main_personality.get_physical_attack_table_index()
        power2 = self.players[1].main_personality.get_physical_attack_table_index()
        if power1 >= 3 and power2 < 3:
            dprint(f'{self.players[1].name} will go first (Power Rule)')
            self.players = list(reversed(self.players))
        elif power1 < 3 and power2 >= 3:
            dprint(f'{self.players[0].name} will go first (Power Rule)')
        else:
            random.shuffle(self.players)
            dprint(f'{self.players[0].name} will go first')

        # Disambiguate player names
        if self.players[0].name == self.players[1].name:
            self.players[0].name = f'{self.players[0].name}-1'
            self.players[1].name = f'{self.players[1].name}-2'

        self.players[0].register_opponent(self.players[1])
        self.players[1].register_opponent(self.players[0])

    def __repr__(self):
        return f'{self.players[0].name} vs {self.players[1].name}'

    def show_summary(self, quiet=None):
        # If quiet is None, we defer to State.QUIET
        summaries = [player.get_summary() for player in reversed(self.players)]
        dprint_table(summaries, quiet=quiet)
        State.IO_BACKEND.write_state(self.build_state_snapshot())

    def build_state_snapshot(self):
        '''JSON-serializable board state for a browser UI (see
        BrowserBackend.write_state). Mirrors the same fields
        Player.get_summary()/show_pile() already gather for the terminal
        table, just shaped as a dict instead of formatted strings.'''
        return {
            'turn': State.TURN + 1,
            'players': [self._player_snapshot(player) for player in reversed(self.players)],
        }

    def _player_snapshot(self, player):
        active_card_powers = player.get_valid_card_powers(CardPower)

        def card_snapshot(card):
            return {'id': card.get_id(), 'name': card.name, 'cardText': card.card_text}

        def personality_snapshot(personality, anger=None):
            snapshot = {
                'id': personality.get_id(),
                'name': personality.char_name(),
                'level': personality.level,
                'powerAttackStr': personality.get_power_attack_str(),
                'cardText': personality.card_text,
                'attachedCards': [card_snapshot(c) for c in personality.attached_cards],
            }
            if anger is not None:
                snapshot['anger'] = anger
            return snapshot

        def dragon_ball_snapshot(card):
            return {
                'id': card.get_id(),
                'name': card.name,
                'dbSet': card.db_set,
                'dbNumber': card.db_number,
                'active': any(x.card is card for x in active_card_powers),
            }

        return {
            'name': player.name,
            'playerNum': player.player_num,
            'interactive': player.interactive,
            'lifeDeckCount': len(player.life_deck),
            'deckSize': player.deck_size,
            'discardCount': len(player.discard_pile),
            'removedCount': len(player.removed_pile),
            'handCount': len(player.hand),
            'hand': ([card_snapshot(c) for c in player.hand]
                     if player.should_show_hand() else None),
            'mainPersonality': personality_snapshot(player.main_personality, anger=player.anger),
            'allies': [personality_snapshot(ally) for ally in player.allies],
            'nonCombat': [card_snapshot(c) for c in player.non_combat],
            'drills': [card_snapshot(c) for c in player.drills],
            'dragonBalls': [dragon_ball_snapshot(c) for c in player.dragon_balls],
            'floatingCardPowers': [
                str(cp) for cp in active_card_powers if cp.is_floating],
        }

    def run(self):
        while True:
            State.COMBAT_ROUND = 0

            try:
                self.take_turn()

            except GameOver as err:
                self.show_summary(quiet=False)
                player_num = (f'{"P" if err.winning_player.interactive else "CPU"}'
                              f'{err.winning_player.player_num}')
                dprint(f'{err.winning_player} ({player_num}) wins!', quiet=False)
                dprint(f'{err}', quiet=False)
                return err.winning_player.player_num

            except DeckEmpty as err:
                for player in self.players:
                    if len(player.life_deck) == 0:
                        self.show_summary(quiet=False)
                        player_num = (f'{"P" if player.opponent.interactive else "CPU"}'
                                      f'{player.opponent.player_num}')
                        dprint(f'{player.opponent} ({player_num}) wins!', quiet=False)
                        dprint(f'{player}\'s Life Deck is empty', quiet=False)
                        return player.opponent.player_num
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

        header = f'Turn {State.TURN+1}: {player}'
        border = '=' * State.PRINT_WIDTH
        dprint(border)
        dprint(f'{"="*10} {header} {border}'[:State.PRINT_WIDTH])
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
