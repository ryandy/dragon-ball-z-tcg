import copy
import sys


class DamageModifier:
    def __init__(self, power_add=None, power_mult=None, power_max=None,
                 life_add=None, life_mult=None, life_max=None, stopped=None,
                 power_prevent=None, life_prevent=None):
        self.power_add = power_add or 0
        self.power_mult = power_mult or 1
        self.power_max = power_max or 1000
        self.life_add = life_add or 0
        self.life_mult = life_mult or 1
        self.life_max = life_max or 1000
        self.stopped = stopped or False
        self.power_prevent = power_prevent or 0
        self.life_prevent = life_prevent or 0

    def __repr__(self):
        return (f'DamageModifier({self.power_add}, {self.power_mult}, {self.power_max}'
                f', {self.life_add}, {self.life_mult}, {self.life_max}, {self.stopped}'
                f', {self.power_prevent}, {self.life_prevent})')

    def copy(self):
        return copy.copy(self)

    @classmethod
    def none(cls):
        return cls()
