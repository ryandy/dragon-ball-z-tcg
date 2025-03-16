import sys

from combat_card import CombatCard
from phase import Phase
from timing import Timing


class CombatAttackPhase(Phase):
    def __init__(self, player):
        self.player = player
        self.passed = True

    def execute(self):
        # TODO give player opportunity to pass

        powers = self.player.powers[Timing.ATTACK]
        if len(powers) == 0:
            return

        print(f'{self.player} has {len(powers)} combat attack choice(s)')
        for card, cost, damage, execute in powers:
            if self.player.can_afford_cost(cost):
                self.passed = False
                execute(card, self.player, self)
                return

    def physical_attack(self, damage, src=None):

        # TODO Defender defends

        if src and True:
            print(f'{self.player} uses {src} for {damage}')
        self.player.opponent.apply_physical_attack_damage(damage)
