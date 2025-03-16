import sys

from combat_attack_phase import CombatAttackPhase
from draw_phase import DrawPhase
from phase import Phase


class CombatPhase(Phase):
    def __init__(self, player):
        self.player = player
        self.passed = True

    def execute(self):
        # TODO give player opportunity to pass
        self.passed = False

        # "WHEN ENTERING COMBAT" (attacker before defender)

        opp_draw_phase = DrawPhase(self.player.opponent, is_defender=True)
        opp_draw_phase.execute()

        pass_count = 0
        attacker = self.player
        while True:
            attack_phase = CombatAttackPhase(attacker)
            attack_phase.execute()
            if attack_phase.passed:
                pass_count += 1
            else:
                pass_count = 0
            if pass_count == 2:
                break
            attacker = attacker.opponent

        # "AT THE END OF COMBAT" (attacker before defender)
