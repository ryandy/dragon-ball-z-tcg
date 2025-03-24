import sys

from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense, CardPowerAnyDefense
from combat_card import CombatCard
from phase import Phase
from timing import Timing
from util import dprint


class CombatDefensePhase(Phase):
    def __init__(self, player):
        self.player = player

    def physical_defense(self, damage):
        '''Returns resulting damage'''
        return self._defense(damage, is_physical=True)

    def energy_defense(self, damage):
        '''Returns resulting damage'''
        return self._defense(damage, is_physical=False)

    def _defense(self, damage, is_physical=None):
        card_power_class = CardPowerPhysicalDefense if is_physical else CardPowerEnergyDefense
        card_power = self.player.choose_card_power(
            [card_power_class, CardPowerAnyDefense],
            prompt='Select a card power for defense')
        if card_power:
            dprint(f'{self.player.name()} uses {card_power} to defend')
            if not self.player.interactive:
                dprint(f'  - {card_power.description}')
            damage = card_power.on_defense(self.player, self, damage)
        else:
            dprint(f'{self.player.name()} has no defense')

        if not damage.was_stopped():
            # Activate a relevant defense shield
            shield_card_power = self.player.choose_defense_shield(is_physical=is_physical)
            if shield_card_power:
                dprint(f'{self.player.name()} activates Defense Shield: {shield_card_power}')
                damage = shield_card_power.on_defense(self.player, self, damage)

        return damage
