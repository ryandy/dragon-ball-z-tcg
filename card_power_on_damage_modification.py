import copy
import sys

from card_power import CardPower
from cost import Cost


class CardPowerOnDamageModification(CardPower):
    def __init__(self, name, description,
                 own_physical=None, own_energy=None,
                 opp_physical=None, opp_energy=None):
        super().__init__(name, description, Cost.none())
        self.own_physical = own_physical
        self.own_energy = own_energy
        self.opp_physical = opp_physical
        self.opp_energy = opp_energy

    def copy(self):
        # Note: do not deep copy self.card
        card_power_copy = copy.copy(self)
        card_power_copy.own_physical = self.own_physical.copy() if self.own_physical else None
        card_power_copy.own_energy = self.own_energy.copy() if self.own_energy else None
        card_power_copy.opp_physical = self.opp_physical.copy() if self.opp_physical else None
        card_power_copy.opp_energy = self.opp_energy.copy() if self.opp_energy else None
        return card_power_copy

    def on_physical_damage_modification(self, attacker, phase):
        if self.own_physical and self.player is attacker:
            return self.own_physical.copy()
        elif self.opp_physical and self.player is not attacker:
            return self.opp_physical.copy()

    def on_energy_damage_modification(self, attacker, phase):
        if self.own_energy and self.player is attacker:
            return self.own_energy.copy()
        elif self.opp_energy and self.player is not attacker:
            return self.opp_energy.copy()
