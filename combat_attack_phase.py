import sys

from card_power_attack import CardPowerAttack
from card_power_on_attack_resolved import CardPowerOnAttackResolved
from card_power_on_damage_modification import CardPowerOnDamageModification
from combat_defense_phase import CombatDefensePhase
from phase import Phase
from state import State
from util import dprint


class CombatAttackPhase(Phase):
    def __init__(self, player, combat_phase, attack_power_override=None):
        self.player = player
        self.combat_phase = combat_phase
        self.attack_power_override = attack_power_override

        self.attack_power = None
        self.passed = False
        self.end_combat = False
        self.skip_next_attack_phase = False
        self.next_attack_power = None  # attack power to be used for the next combat attack phase

    def execute(self):
        State.PHASE = self

        # Very rarely an attack power will be pre-selected for the attack phase
        if self.attack_power_override:
            self.attack_power = self.attack_power_override
        else:
            self.player.determine_control_of_combat()
            self.attack_power = self.player.choose_card_power(CardPowerAttack)

        if not self.attack_power:
            self.passed = True
            dprint(f'{self.player} passes')
            self.player.card_powers_played_this_combat.append(None)
            return

        # Log the card used
        self.player.card_powers_played_this_combat.append(self.attack_power.copy())
        if self.attack_power.card and not self.attack_power.is_floating:
            self.player.cards_played_this_combat.append(self.attack_power.card)

        damage_mod_srcs = []
        if self.attack_power.is_physical is None:  # Non-combat attacks
            dprint(f'{self.player} uses {self.attack_power} (Non-Combat)')
        else:
            dprint(f'{self.player} attacks with {self.attack_power}')
        if not self.player.interactive:
            dprint(f'  - {self.attack_power.description}')

        # Choose if an ally (of the defender) will take control of combat
        # Note: This needs to happen here rather than combat_defense_phase so that the choice can
        #       be made before any secondary effects from the attack take place.
        self.player.opponent.determine_control_of_combat()

        self.attack_power.on_attack(self.player, self)

        # Control reverts to MP for either attacker or defender if MP power >= 2
        for player in State.gen_players():
            player.revert_control_of_combat_if_able()

    def set_force_end_combat(self):
        self.combat_phase.set_force_end_combat()

    def set_skip_next_attack_phase(self):
        self.skip_next_attack_phase = True

    def set_next_attack_power(self, next_attack_power):
        self.next_attack_power = next_attack_power

    def physical_attack(self, damage):
        '''Returns True if attack was successful'''
        return self._attack(damage, is_physical=True)

    def energy_attack(self, damage):
        '''Returns True if attack was successful'''
        return self._attack(damage, is_physical=False)

    def _attack(self, damage, is_physical=None):
        # Damage estimate is most helpful/accurate here
        damage_estimate, damage_mod_srcs = self._get_damage(self.attack_power.damage)
        dprint(f'{self.player}\'s attack damage estimate: {damage_estimate}')
        if damage_mod_srcs:
            for damage_mod_src in damage_mod_srcs:
                dprint(f'  - Damage modified by {damage_mod_src}')

        defense_phase = CombatDefensePhase(self.player.opponent, self.combat_phase, self)
        if is_physical:
            damage = defense_phase.physical_defense(damage)
        else:
            damage = defense_phase.energy_defense(damage)
        State.PHASE = self

        # Refresh damage mods
        damage, _ = self._get_damage(damage)
        damage_applied = damage.copy()

        if not damage.was_stopped():
            if is_physical:
                damage_applied = self.player.opponent.apply_physical_attack_damage(
                    damage, src_personality=self.player.control_personality)
            else:
                damage_applied = self.player.opponent.apply_energy_attack_damage(
                    damage, src_personality=self.player.control_personality)

        for player in State.gen_players():
            card_powers = player.get_valid_card_powers(CardPowerOnAttackResolved)
            for card_power in card_powers:
                card_power.on_attack_resolved(self, damage_applied, is_physical)

        return not damage.was_stopped()

    def _get_damage(self, base_damage):
        # Check for active DamageModification card powers
        damage_mods = []
        damage_mod_srcs = []
        for player in State.gen_players():
            odm_card_powers = player.get_valid_card_powers(CardPowerOnDamageModification)
            for odm_card_power in odm_card_powers:
                if self.attack_power.is_physical is True:
                    mod = odm_card_power.on_physical_damage_modification(self.player, self)
                    if mod:
                        damage_mods.append(mod)
                        damage_mod_srcs.append(f'{player}\'s: {odm_card_power}')
                elif self.attack_power.is_physical is False:
                    mod = odm_card_power.on_energy_damage_modification(self.player, self)
                    if mod:
                        damage_mods.append(mod)
                        damage_mod_srcs.append(f'{player}\'s: {odm_card_power}')
        damage_copy = base_damage.copy()
        damage_copy.modify(damage_mods)
        return damage_copy.resolve(self.player), damage_mod_srcs
