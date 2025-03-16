import sys


class Cost:
    def __init__(self, power, life, friendly_ally=None, any_ally=None, specific_ally=None):
        self.power = power
        self.life = life
        self.friendly_ally = friendly_ally
        self.any_ally = any_ally
        self.specific_ally = specific_ally

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
