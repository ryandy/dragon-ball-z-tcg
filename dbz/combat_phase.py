import sys

from dbz.card_power_on_entering_combat import CardPowerOnEnteringCombat
from dbz.card_power_on_combat_declared import CardPowerOnCombatDeclared
from dbz.combat_attack_phase import CombatAttackPhase
from dbz.draw_phase import DrawPhase
from dbz.phase import Phase
from dbz.state import State
from dbz.util import dprint


class CombatPhase(Phase):
    def __init__(self, runner, player, power_up_phase):
        self.runner = runner
        self.player = player
        self.skipped = power_up_phase.force_skip_combat
        self.force_end_combat = False

    def set_force_end_combat(self):
        self.force_end_combat = True

    def set_force_skip_phase(self):
        self.skipped = True

    def entering_combat(self):
        State.ATTACKING_PLAYER = self.player

        for player in State.gen_players():
            player.cards_played_this_combat = []
            player.card_powers_played_this_combat = []
            card_powers = player.get_valid_card_powers(CardPowerOnEnteringCombat)
            for card_power in card_powers:
                card_power.on_entering_combat(self)

    def end_of_combat(self):
        State.ATTACKING_PLAYER = None

        for player in State.gen_players():
            player.revert_control_of_combat()
            player.cards_played_this_combat = []
            player.card_powers_played_this_combat = []

    def execute(self):
        State.PHASE = self

        if self.skipped:
            # Choice of declaring combat was prevented before combat phase began
            dprint(f'{self.player} cannot declare combat')
        else:
            self.skipped = not self.player.choose_declare_combat()
            if self.skipped:
                dprint(f'{self.player} chooses to skip combat')

        if not self.skipped:
            for player in State.gen_players():
                card_powers = player.get_valid_card_powers(CardPowerOnCombatDeclared)
                for card_power in card_powers:
                    card_power.on_combat_declared(self)

        if self.skipped:
            return
        else:
            dprint(f'{self.player} declares combat!')

        self.entering_combat()

        opp_draw_phase = DrawPhase(self.player.opponent, is_attacker=False)
        opp_draw_phase.execute()

        State.PASS_COUNT = 0
        next_attack_power = None  # Will almost always be None
        while True:
            # End Combat Phase when two players pass consecutively or the phase is forcibly ended
            if State.PASS_COUNT == 2 or self.force_end_combat:
                break

            header = f'Attack Phase {State.TURN+1}.{State.COMBAT_ROUND+1}: {State.ATTACKING_PLAYER}'
            border = '-' * State.PRINT_WIDTH
            dprint()
            dprint(f'{"-"*10} {header} {border}'[:State.PRINT_WIDTH])
            self.runner.show_summary()

            attack_phase = CombatAttackPhase(
                State.ATTACKING_PLAYER, self, attack_power_override=next_attack_power)
            attack_phase.execute()

            if attack_phase.passed:
                State.PASS_COUNT += 1
            else:
                State.PASS_COUNT = 0

            # Check to see if the next player's attack phase should be skipped
            # Note: Skipping is different than forced passing (e.g. after FPA) because it does
            #       not contribute toward the pass_count == 2 check
            if attack_phase.skip_next_attack_phase:
                State.COMBAT_ROUND += 2
            else:
                State.ATTACKING_PLAYER = State.ATTACKING_PLAYER.opponent
                State.COMBAT_ROUND += 1

            # Will almost always be None
            next_attack_power = attack_phase.next_attack_power

        self.end_of_combat()
