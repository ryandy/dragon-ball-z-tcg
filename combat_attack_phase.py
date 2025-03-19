import sys

from card_power_attack import CardPowerAttack
from combat_defense_phase import CombatDefensePhase
from phase import Phase


class CombatAttackPhase(Phase):
    def __init__(self, player):
        self.player = player
        self.passed = True

    def execute(self):
        card_power = self.player.card_power_choice(CardPowerAttack)
        if card_power:
            self.passed = False
            card_power.on_attack(self.player, self)
        #print()

    def physical_attack(self, damage, src=None):
        '''Returns True if attack was successful'''
        return self._attack(damage, src=src, is_physical=True)

    def energy_attack(self, damage, src=None):
        '''Returns True if attack was successful'''
        return self._attack(damage, src=src, is_physical=False)

    def _attack(self, damage, src=None, is_physical=None):
        print(f'{self.player} uses {src} for {damage}')

        defense_phase = CombatDefensePhase(self.player.opponent)
        if is_physical:
            damage = defense_phase.physical_defense(damage)
        else:
            damage = defense_phase.energy_defense(damage)

        if not damage.was_stopped():
            if is_physical:
                self.player.opponent.apply_physical_attack_damage(damage)
            else:
                self.player.opponent.apply_energy_attack_damage(damage)

        return not damage.was_stopped()
