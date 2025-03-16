import sys


class Damage:
    def __init__(self, power_base=0, power_add=0, power_mult=1, life_base=0, life_add=0, use_pat=0):
        self.power_base = power_base
        self.power_add = power_add
        self.power_mult = power_mult
        self.life_base = life_base
        self.life_add = life_add
        self.use_pat = use_pat

    def __repr__(self):
        power, life = '', ''
        if self.power_base or self.power_add or self.power_mult!=1 or self.use_pat:
            if self.use_pat:
                power = 'PAT'
            else:
                power = f'{self.power_base or 0}'
            if self.power_mult != 1:
                power = f'{power}*{self.power_mult}'
            if self.power_add > 0:
                power = f'{power}+{self.power_add}'
            elif self.power_add < 0:
                power = f'{power}-{-self.power_add}'
        if self.life_base or self.life_add:
            life = f'{self.life_base or 0}'
            if self.life_add > 0:
                life = f'{life}+{self.life_add}'
            elif self.life_add < 0:
                life = f'{life}-{-self.life_add}'
        power = power or '0'
        life = life or '0'
        return f'Damage({power}, {life})'

    def calculate(self, attacker):
        power, life = self.power_base, self.life_base
        if self.use_pat:
            attack_idx = attacker.personality.get_physical_attack_table_index()
            defend_idx = attacker.opponent.personality.get_physical_attack_table_index()
            power += max(0, 1 + attack_idx - defend_idx)
        power *= self.power_mult
        power += self.power_add
        life += self.life_add
        return power, life

    @classmethod
    def energy_attack(cls, power_base=None, life_base=None, use_pat=False):
        power_base = 0 if power_base is None else power_base
        life_base = 4 if life_base is None else life_base
        return cls(power_base=power_base, life_base=life_base, use_pat=use_pat)

    @classmethod
    def physical_attack(cls, power_base=None, life_base=None, use_pat=True):
        power_base = 0 if power_base is None else power_base
        life_base = 0 if life_base is None else life_base
        return cls(power_base=power_base, life_base=life_base, use_pat=use_pat)

    # TODO: Needs its own class?
    # TODO: If this stays, need a way to "add" this to another damage instance
    @classmethod
    def life_damage_reduction(cls, life_reduction):
        return cls(life_add=-life_reduction)
