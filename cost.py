import copy
import sys

from character import Character


class Cost:
    def __init__(self, power=None, life=None, character_in_control_req=None):
        # Costs:
        self.power = power or 0
        self.life = life or 0

        # Requirements:
        self.character_in_control_req = character_in_control_req or []  # [Character,]
        if isinstance(self.character_in_control_req, Character):
            self.character_in_control_req = [self.character_in_control_req]

    def copy(self):
        return copy.copy(self)

    @classmethod
    def none(cls):
        return Cost()

    @classmethod
    def energy_attack(cls, power=None, life=None):
        if power is not None or life is not None:
            power = power or 0
            life = life or 0
        else:
            power = 2
            life = 0
        return cls(power=power, life=life)
