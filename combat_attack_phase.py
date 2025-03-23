import sys

from card_power_attack import CardPowerAttack
from card_power_on_damage_modification import CardPowerOnDamageModification
from combat_defense_phase import CombatDefensePhase
from phase import Phase
from util import dprint


class CombatAttackPhase(Phase):
    def __init__(self, player):
        self.player = player
        self.passed = False
        self.attack_power = None
        self.combat_ended = False

    def execute(self):
        self.attack_power = self.player.choose_card_power(CardPowerAttack)
        if not self.attack_power:
            self.passed = True
            dprint(f'{self.player.name()} passes')
            return

        damage_mod_srcs = []
        if self.attack_power.is_physical is None:  # Non-combat attacks
            dprint(f'{self.player.name()} uses {self.attack_power} (Non-Combat)')
        else:
            dprint(f'{self.player.name()} attacks with {self.attack_power}')
        if not self.player.interactive:
            dprint(f'  - {self.attack_power.description}')

        self.attack_power.on_attack(self.player, self)

    def end_combat(self):
        self.combat_ended = True

    def physical_attack(self, damage):
        '''Returns True if attack was successful'''
        return self._attack(damage, is_physical=True)

    def energy_attack(self, damage):
        '''Returns True if attack was successful'''
        return self._attack(damage, is_physical=False)

    def _attack(self, damage, is_physical=None):
        # Damage estimate is most helpful/accurate here
        damage_estimate, damage_mod_srcs = self._get_damage(self.attack_power.damage)
        dprint(f'{self.player.name()}\'s attack damage estimate: {damage_estimate}')
        if damage_mod_srcs:
            for damage_mod_src in damage_mod_srcs:
                dprint(f'  - Damage modified by {damage_mod_src}')

        defense_phase = CombatDefensePhase(self.player.opponent)
        if is_physical:
            damage = defense_phase.physical_defense(damage)
        else:
            damage = defense_phase.energy_defense(damage)

        # TODO: on_attack_resolved

        if not damage.was_stopped():
            # Refresh damage mods
            final_damage, _ = self._get_damage(damage)

            if is_physical:
                self.player.opponent.apply_physical_attack_damage(final_damage)
            else:
                self.player.opponent.apply_energy_attack_damage(final_damage)

        return not damage.was_stopped()

    def _get_damage(self, base_damage):
        # Check for active DamageModification card powers
        damage_mods = []
        damage_mod_srcs = []
        for player in [self.player, self.player.opponent]:
            odm_card_powers = player.get_valid_card_powers(CardPowerOnDamageModification)
            for odm_card_power in odm_card_powers:
                if self.attack_power.is_physical is True:
                    mod = odm_card_power.on_physical_damage_modification(self.player, self)
                    if mod:
                        damage_mods.append(mod)
                        damage_mod_srcs.append(f'{player.name()}\'s: {odm_card_power}')
                elif self.attack_power.is_physical is False:
                    mod = odm_card_power.on_energy_damage_modification(self.player, self)
                    if mod:
                        damage_mods.append(mod)
                        damage_mod_srcs.append(f'{player.name()}\'s: {odm_card_power}')
        damage_copy = base_damage.copy()
        damage_copy.modify(damage_mods)
        return damage_copy.resolve(self.player), damage_mod_srcs
