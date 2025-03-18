import sys


class Damage:
    def __init__(self, power=None, life=None, use_pat=None, mods=None):
        assert (not power or not use_pat)
        self.power = power or 0
        self.life = life or 0
        self.use_pat = use_pat or False
        self.mods = mods or []

    def __repr__(self):
        power = 'PAT' if self.use_pat else self.power
        return f'Damage({power}, {self.life})'

    def modify(self, mod):
        self.mods.append(mod)

    def was_stopped(self):
        return any(x.stopped for x in self.mods)

    def calculate(self, attacker):
        if self.was_stopped():
            return 0, 0

        power, life = self.power, self.life
        if self.use_pat:
            attack_idx = attacker.personality.get_physical_attack_table_index()
            defend_idx = attacker.opponent.personality.get_physical_attack_table_index()
            power = max(0, 1 + attack_idx - defend_idx)

        for mod in self.mods:
            power += mod.power_add
            life += mod.life_add
        for mod in self.mods:
            power *= mod.power_mult
            life *= life.life_mult
        for mod in self.mods:
            power = min(power, mod.power_max)
            life = min(life, mod.life_max)

        return max(0, power), max(0, life)

    @classmethod
    def energy_attack(cls, life=4):
        return cls(life=life)

    @classmethod
    def physical_attack(cls, power=0, use_pat=True):
        return cls(power=power, use_pat=use_pat)
