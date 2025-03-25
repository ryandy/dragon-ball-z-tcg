import sys

from card_power_on_combat_declared import CardPowerOnCombatDeclared
from combat_attack_phase import CombatAttackPhase
from draw_phase import DrawPhase
from phase import Phase
from state import State
from util import dprint


class CombatPhase(Phase):
    def __init__(self, player, players):
        self.player = player
        self.players = players
        self.skipped = True

    def entering_combat(self):
        pass

    def end_of_combat(self):
        for player in [self.player, self.player.opponent]:
            player.revert_control_of_combat()

    def execute(self):
        self.skipped = not self.player.choose_declare_combat()

        if self.skipped:
            dprint(f'{self.player} chooses to skip combat')

        if not self.skipped:
            for player in [self.player, self.player.opponent]:
                card_powers = player.get_valid_card_powers(CardPowerOnCombatDeclared)
                for card_power in card_powers:
                    card_power.on_combat_declared(player, self)

        if self.skipped:
            return
        else:
            dprint(f'{self.player} declares combat!')

        self.entering_combat()

        opp_draw_phase = DrawPhase(self.player.opponent)
        opp_draw_phase.execute()

        pass_count = 0
        attacker = self.player
        next_attack_power = None  # Will almost always be None
        while True:
            dprint()
            dprint(f'---------- Attack Phase {State.TURN+1}.{State.COMBAT_ROUND+1}:'
                   f' {attacker} ----------')
            for player in self.players:
                player.show_summary()

            attack_phase = CombatAttackPhase(attacker, attack_power_override=next_attack_power)
            attack_phase.execute()

            if attack_phase.passed:
                pass_count += 1
            else:
                pass_count = 0

            # End Combat Phase when two players pass consecutively or the phase is forcibly ended
            if pass_count == 2 or attack_phase.end_combat:
                break

            # Check to see if the next player's attack phase should be skipped
            if attack_phase.skip_next_attack_phase:
                State.COMBAT_ROUND += 2
            else:
                attacker = attacker.opponent
                State.COMBAT_ROUND += 1

            # Will almost always be None
            next_attack_power = attack_phase.next_attack_power

        self.end_of_combat()
