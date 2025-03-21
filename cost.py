import copy
import sys


class Cost:
    def __init__(self, power, life):
        # TODO: can also handle discard/ally/drill/etc costs
        self.power = power
        self.life = life

    def copy(self):
        return copy.copy(self)

    @classmethod
    def none(cls):
        return Cost(0, 0)

    @classmethod
    def energy_attack(cls, power=None, life=None):
        if power is not None or life is not None:
            power = power or 0
            life = life or 0
        else:
            power = 2
            life = 0
        return cls(power, life)
