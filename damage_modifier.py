import copy
import sys


class DamageModifier:
    def __init__(self, power_add=None, power_mult=None, power_max=None,
                 life_add=None, life_mult=None, life_max=None, stopped=None):
        self.power_add = power_add or 0
        self.power_mult = power_mult or 1
        self.power_max = power_max or 1000
        self.life_add = life_add or 0
        self.life_mult = life_mult or 1
        self.life_max = life_max or 1000
        self.stopped = stopped or False

    def copy(self):
        return copy.copy(self)
