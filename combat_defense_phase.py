import sys

from combat_card import CombatCard
from phase import Phase
from timing import Timing


class CombatDefensePhase(Phase):
    def __init__(self, player):
        self.player = player
        self.attack_successful = False

    def register_damage_modifier(self, damage_modifier):
        self.damage_modifier = damage_modifier

    def execute_physical_defense(self, damage, src=None):
        '''Returns True if attack was stopped'''
        # TODO: player should be able to pass

        powers = self.player.powers[Timing.PHYSICAL_DEFENSE]
        print(f'{self.player} has {len(powers)} physical defense choice(s)')
        for card, cost, _, execute in powers:
            if self.player.can_afford_cost(cost):
                execute(card, cost, damage, self.player, self)
                return True

        self.attack_successful = True

        powers = self.player.powers[Timing.PHYSICAL_DAMAGE_REDUCTION]
        print(f'{self.player} has {len(powers)} physical damage reduction choice(s)')
        for card, cost, _, execute in powers:
            if self.player.can_afford_cost(cost):
                execute(card, cost, damage, self.player, self)
                break

        return False

    # TODO
    def execute_energy_defense(self, damage, src=None):
        '''Returns True if attack was stopped'''

        powers = self.player.powers[Timing.ENERGY_DEFENSE]
        print(f'{self.player} has {len(powers)} energy defense choice(s)')
        for card, cost, _, execute in powers:
            if self.player.can_afford_cost(cost):
                execute(card, cost, damage, self.player, self)
                return True

        powers = self.player.powers[Timing.ENERGY_DAMAGE_REDUCTION]
        print(f'{self.player} has {len(powers)} energy damage reduction choice(s)')
        for card, cost, _, execute in powers:
            if self.player.can_afford_cost(cost):
                execute(card, cost, damage, self.player, self)
                break

        return False
