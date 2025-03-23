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

    def execute(self):
        self.skipped = not self.player.choose_declare_combat()

        if self.skipped:
            dprint(f'{self.player.name()} chooses to skip combat')

        if not self.skipped:
            for player in [self.player, self.player.opponent]:
                card_powers = player.get_valid_card_powers(CardPowerOnCombatDeclared)
                for card_power in card_powers:
                    card_power.on_combat_declared(player, self)

        if self.skipped:
            return
        else:
            dprint(f'{self.player.name()} declares combat!')

        # "WHEN ENTERING COMBAT" (attacker before defender)

        opp_draw_phase = DrawPhase(self.player.opponent)
        opp_draw_phase.execute()

        pass_count = 0
        attacker = self.player
        while True:
            dprint()
            dprint(f'---------- Attack Phase {State.COMBAT_ROUND+1}: {attacker.name()} ----------')
            for player in self.players:
                player.show_summary()

            attack_phase = CombatAttackPhase(attacker)
            attack_phase.execute()

            if attack_phase.passed:
                pass_count += 1
            else:
                pass_count = 0
            if pass_count == 2:
                break
            if attack_phase.combat_ended:
                break
            attacker = attacker.opponent
            State.COMBAT_ROUND += 1

        # TODO: Control reverts to MP for both players

        # "AT THE END OF COMBAT" (attacker before defender)
