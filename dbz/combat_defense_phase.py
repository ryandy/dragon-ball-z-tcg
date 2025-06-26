import sys

from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense, CardPowerAnyDefense
from dbz.combat_card import CombatCard
from dbz.phase import Phase
from dbz.state import State
from dbz.util import dprint


class CombatDefensePhase(Phase):
    def __init__(self, player, combat_phase, attack_phase):
        self.player = player
        self.combat_phase = combat_phase
        self.attack_phase = attack_phase

    def set_force_end_combat(self):
        self.combat_phase.set_force_end_combat()

    def physical_defense(self, damage):
        '''Returns resulting damage'''
        State.PHASE = self
        return self._defense(damage, is_physical=True)

    def energy_defense(self, damage):
        '''Returns resulting damage'''
        State.PHASE = self
        return self._defense(damage, is_physical=False)

    def _defense(self, damage, is_physical=None):
        # TODO: AI needs access to damage when choosing a defense
        card_power_class = CardPowerPhysicalDefense if is_physical else CardPowerEnergyDefense
        card_power = self.player.choose_card_power(
            [card_power_class, CardPowerAnyDefense],
            prompt='Select a card power for defense')

        if card_power:
            # Log the card used
            self.player.card_powers_played_this_combat.append(card_power.copy())
            if card_power.card and not card_power.is_floating:
                self.player.cards_played_this_combat.append(card_power.card)
            dprint(f'{self.player} uses {card_power} to defend')
            if not self.player.interactive:
                dprint(f'  - {card_power.description}')
            damage = card_power.on_defense(self.player, self, damage)
        else:
            dprint(f'{self.player} has no defense')
            self.player.card_powers_played_this_combat.append(None)

        if not damage.was_stopped():
            # Activate a relevant defense shield
            shield_card_power = self.player.choose_defense_shield(is_physical=is_physical)
            if shield_card_power:
                # Log the card used
                self.player.card_powers_played_this_combat.append(shield_card_power.copy())
                if shield_card_power.card and not shield_card_power.is_floating:
                    self.player.cards_played_this_combat.append(shield_card_power.card)
                dprint(f'{self.player} activates Defense Shield: {shield_card_power}')
                damage = shield_card_power.on_defense(self.player, self, damage)

        return damage
