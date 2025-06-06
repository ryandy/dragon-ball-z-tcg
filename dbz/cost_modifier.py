import copy
import sys


class CostModifier:
    def __init__(self, power_ittt=None):
        self.power_ittt = power_ittt or dict()

    def __repr__(self):
        return (f'CostModifier({self.power_ittt})')

    def copy(self):
        return copy.copy(self)

    @classmethod
    def none(cls):
        return cls()
