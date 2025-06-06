import copy
import sys

from dbz.card_power import CardPower
from dbz.card_power_attack import CardPowerEnergyAttack
from dbz.cost import Cost


class CardPowerOnCostModification(CardPower):
    def __init__(self, name, description, own_energy=None, opp_energy=None):
        super().__init__(name, description, Cost.none())
        self.own_energy = own_energy
        self.opp_energy = opp_energy

    def copy(self):
        # Note: do not deep copy self.card
        card_power_copy = copy.copy(self)
        card_power_copy.own_energy = self.own_energy.copy() if self.own_energy else None
        card_power_copy.opp_energy = self.opp_energy.copy() if self.opp_energy else None
        return card_power_copy

    def on_cost_modification(self, player, card_power):
        if isinstance(card_power, CardPowerEnergyAttack):
            if self.own_energy and self.player is player:
                return self.own_energy.copy()
            if self.opp_energy and self.player is not player:
                return self.opp_energy.copy()
