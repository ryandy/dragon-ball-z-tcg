import sys

from card_power_attack import CardPowerAttack
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

    def physical_attack(self, damage, src=None):
        #defense_phase = CombatDefensePhase(self.player.opponent)
        #attack_stopped = defense_phase.execute_physical_defense(damage)

        #if defense_phase.damage_modifier:
        #    # TODO modify damage
        #    pass

        if src:
            print(f'{self.player} uses {src} for {damage}')

        self.player.opponent.apply_physical_attack_damage(damage)
        #return not attack_stopped
        return True

    def energy_attack(self, damage, src=None):
        # TODO Defender defends
        if src:
            print(f'{self.player} uses {src} for {damage}')
        self.player.opponent.apply_energy_attack_damage(damage)
        return True
