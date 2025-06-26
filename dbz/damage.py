import sys


class Damage:
    def __init__(self, power=None, life=None, use_pat=None, mods=None, stopped=None,
                 power_prevent=None, life_prevent=None, life_prevent_and_draw=None):
        assert (not power or not use_pat)
        self.power = power or 0
        self.life = life or 0
        self.use_pat = use_pat or False
        self.mods = mods or []
        self.stopped = stopped or False
        self.power_prevent = power_prevent or 0
        self.life_prevent = life_prevent or 0
        self.life_prevent_and_draw = life_prevent_and_draw or 0

    @classmethod
    def _add_prevent_mods(cls, a, b):
        if a >= 0 and b >= 0:
            return a + b
        if a < 0 and b < 0:
            # e.g. prevent-all-but-1 + prevent-all-but-3 = prevent-all-but-1
            return max(a, b)
        if a + b < 0:
            # e.g. prevent-all-but-3 + prevent-1 = prevent-all-but-2
            return a + b
        # e.g. prevent-all-but-1 + prevent-2 = prevent-all
        return 1000

    def __repr__(self):
        stopped = self.was_stopped()
        if stopped:
            return f'Damage(STOPPED)'

        power = 'PAT' if self.use_pat else f'{self.power}'
        life = f'{self.life}'
        power_add, life_add, power_mult, life_mult, power_max, life_max = 0, 0, 1, 1, 1000, 1000
        power_prevent = self.power_prevent
        life_prevent = self._add_prevent_mods(self.life_prevent, self.life_prevent_and_draw)
        for mod in self.mods:
            power_add += mod.power_add
            life_add += mod.life_add
            power_mult = max(power_mult, mod.power_mult)  # mults do not stack
            life_mult = max(life_mult, mod.life_mult)  # mults do not stack
            power_max = min(power_max, mod.power_max)
            life_max = min(life_max, mod.life_max)
            power_prevent = self._add_prevent_mods(power_prevent, mod.power_prevent)
            life_prevent = self._add_prevent_mods(life_prevent, mod.life_prevent)
            life_prevent = self._add_prevent_mods(life_prevent, mod.life_prevent_and_draw)

        if power_mult != 1:
            power = f'{power}*{power_mult}'
        if power_add != 0:
            power = f'{power}+({power_add})'
        if power_prevent != 0:
            power = f'{power}-{power_prevent}'
        if power_max != 1000:
            power = f'min({power},{power_max})'

        if life_mult != 1:
            life = f'{life}*{life_mult}'
        if life_add != 0:
            life = f'{life}+({life_add})'
        if life_prevent != 0:
            life = f'{life}-{life_prevent}'
        if life_max != 1000:
            life = f'min({life},{life_max})'

        return f'Damage({power}, {life})'

    def copy(self):
        return Damage(
            power=self.power,
            life=self.life,
            use_pat=self.use_pat,
            mods=[m.copy() for m in self.mods],
            stopped=self.stopped,
            power_prevent=self.power_prevent,
            life_prevent=self.life_prevent,
            life_prevent_and_draw=self.life_prevent_and_draw)

    def is_none(self):
        return (self.power <= 0
                and self.life <= 0
                and not self.use_pat
                and not any(x.power_add > 0 for x in self.mods)
                and not any(x.life_add > 0 for x in self.mods))

    def modify(self, mod):
        # TODO return new Damage instance
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
            attack_idx = attacker.control_personality.get_physical_attack_table_index()
            defend_idx = attacker.opponent.control_personality.get_physical_attack_table_index()
            power = max(0, 1 + attack_idx - defend_idx)

        power_mult, life_mult = 1, 1
        for mod in self.mods:
            power_mult = max(power_mult, mod.power_mult)  # mults do not stack
            life_mult = max(life_mult, mod.life_mult)  # mults do not stack
        power *= power_mult
        life *= life_mult
        for mod in self.mods:
            power += mod.power_add
            life += mod.life_add
        for mod in self.mods:
            power = min(power, mod.power_max)
            life = min(life, mod.life_max)

        power_prevent, life_prevent, life_prevent_and_draw = (
            self.power_prevent, self.life_prevent, self.life_prevent_and_draw)
        for mod in self.mods:
            power_prevent += mod.power_prevent
            life_prevent = self._add_prevent_mods(life_prevent, mod.life_prevent)
            life_prevent_and_draw = self._add_prevent_mods(
                life_prevent_and_draw, mod.life_prevent_and_draw)

        return Damage(power=max(0, power),
                      life=max(0, life),
                      power_prevent=power_prevent,
                      life_prevent=life_prevent,
                      life_prevent_and_draw=life_prevent_and_draw)

    @classmethod
    def none(cls):
        return cls()

    @classmethod
    def energy_attack(cls, life=4):
        return cls(life=life)

    @classmethod
    def physical_attack(cls, power=0, use_pat=True):
        return cls(power=power, use_pat=use_pat)
