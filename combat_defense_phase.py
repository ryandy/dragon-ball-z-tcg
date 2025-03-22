import sys

from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from combat_card import CombatCard
from phase import Phase
from timing import Timing


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
        card_power = self.player.choose_card_power(card_power_class)
        if card_power:
            damage = card_power.on_defense(self.player, self, damage)
        return damage
