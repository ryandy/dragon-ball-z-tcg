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
        self.combat_ended = False

    def execute(self):
        card_power = self.player.choose_card_power(CardPowerAttack)
        if not card_power:
            self.passed = True
            dprint(f'{self.player.name()} passes')
            return

        # Check for active DamageModification card powers
        damage_mods = []
        damage_mod_srcs = []
        for player in [self.player, self.player.opponent]:
            odm_card_powers = player.get_valid_card_powers(CardPowerOnDamageModification)
            for odm_card_power in odm_card_powers:
                if card_power.is_physical is True:
                    mod = odm_card_power.on_physical_damage_modification(self.player, self)
                    if mod:
                        damage_mods.append(mod)
                        damage_mod_srcs.append(f'{player.name()}\'s {odm_card_power}')
                elif card_power.is_physical is False:
                    mod = odm_card_power.on_energy_damage_modification(self.player, self)
                    if mod:
                        damage_mods.append(mod)
                        damage_mod_srcs.append(f'{player.name()}\'s {odm_card_power}')

        if card_power.is_physical is None:  # Non-combat attacks
            dprint(f'{self.player.name()} uses {card_power} (Non-Combat)')
        else:
            # Provide damage estimate based on card power damage and known damage mods
            damage_copy = card_power.damage.copy()
            damage_copy.modify(damage_mods)
            dprint(f'{self.player.name()} attacks with {card_power} for'
                   f' {damage_copy.resolve(self.player)}')
        if not self.player.interactive:
            dprint(f'  - {card_power.description}')
        if damage_mod_srcs:
            for damage_mod_src in damage_mod_srcs:
                dprint(f'  - Damage modified by {damage_mod_src}')

        card_power.on_attack(self.player, self, damage_mods=damage_mods)

    def end_combat(self):
        self.combat_ended = True

    def physical_attack(self, damage, src=None):
        '''Returns True if attack was successful'''
        return self._attack(damage, src=src, is_physical=True)

    def energy_attack(self, damage, src=None):
        '''Returns True if attack was successful'''
        return self._attack(damage, src=src, is_physical=False)

    def _attack(self, damage, src=None, is_physical=None):
        defense_phase = CombatDefensePhase(self.player.opponent)
        if is_physical:
            damage = defense_phase.physical_defense(damage)
        else:
            damage = defense_phase.energy_defense(damage)

        # TODO: on_attack_resolved

        if not damage.was_stopped():
            if is_physical:
                self.player.opponent.apply_physical_attack_damage(damage)
            else:
                self.player.opponent.apply_energy_attack_damage(damage)

        return not damage.was_stopped()
