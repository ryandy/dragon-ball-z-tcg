import sys


class Damage:
    def __init__(self, power=None, life=None, use_pat=None, mods=None, stopped=None):
        assert (not power or not use_pat)
        self.power = power or 0
        self.life = life or 0
        self.use_pat = use_pat or False
        self.mods = mods or []
        self.stopped = stopped or False

    def __repr__(self):
        stopped = self.was_stopped()
        if stopped:
            return f'Damage(STOPPED)'

        power = 'PAT' if self.use_pat else f'{self.power}'
        life = f'{self.life}'
        power_add, life_add, power_mult, life_mult = 0, 0, 1, 1
        for mod in self.mods:
            power_add += mod.power_add
            life_add += mod.life_add
            power_mult *= mod.power_mult
            life_mult *= mod.life_mult
        if power_mult != 1:
            power = f'{power}*{power_mult}'
        if power_add != 0:
            power = f'{power}+{power_add}'
        if life_mult != 1:
            life = f'{life}*{life_mult}'
        if life_add != 0:
            life = f'{life}+{life_add}'
        return f'Damage({power}, {life})'

    def copy(self):
        return Damage(
            power=self.power,
            life=self.life,
            use_pat=self.use_pat,
            mods=[m.copy() for m in self.mods],
            stopped=self.stopped)

    def modify(self, mod):
        if isinstance(mod, list):
            self.mods.extend(mod)
        else:
            self.mods.append(mod)

    def was_stopped(self):
        return self.stopped or any(x.stopped for x in self.mods)

    def resolve(self, attacker):
        if self.was_stopped():
            return Damage(stopped=True)

        power, life = self.power, self.life
        if self.use_pat:
            attack_idx = attacker.personality.get_physical_attack_table_index()
            defend_idx = attacker.opponent.personality.get_physical_attack_table_index()
            power = max(0, 1 + attack_idx - defend_idx)

        for mod in self.mods:
            power *= mod.power_mult
            life *= mod.life_mult
        for mod in self.mods:
            power += mod.power_add
            life += mod.life_add
        for mod in self.mods:
            power = min(power, mod.power_max)
            life = min(life, mod.life_max)

        return Damage(power=max(0, power), life=max(0, life))

    @classmethod
    def none(cls):
        return cls()

    @classmethod
    def energy_attack(cls, life=4):
        return cls(life=life)

    @classmethod
    def physical_attack(cls, power=0, use_pat=True):
        return cls(power=power, use_pat=use_pat)
