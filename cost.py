import copy
import sys

from character import Character
from state import State


class Cost:
    def __init__(self, power=None, life=None,
                 discard=None,
                 own_ally=None, any_ally=None):
        self.power = power or 0
        self.life = life or 0
        self.discard = discard or 0
        self.own_ally = own_ally or 0
        self.any_ally = any_ally or 0

    def copy(self):
        return copy.copy(self)

    def is_none(self):
        return (self.power == 0
                and self.life == 0
                and self.discard == 0
                and self.own_ally == 0
                and self.any_ally == 0)

    # Note: cannot import CardPowerOnCostModification without creating a circular dep..
    def resolve(self, payer, card_power, mod_class):
        cost_mods = []
        cost_mod_srcs = []
        for ocm_player in State.gen_players():
            ocm_card_powers = ocm_player.get_valid_card_powers(mod_class)
            for ocm_card_power in ocm_card_powers:
                mod = ocm_card_power.on_cost_modification(payer, card_power)
                if mod:
                    cost_mods.append(mod)
                    cost_mod_srcs.append(f'{ocm_player}\'s {ocm_card_power}')

        if not cost_mods:
            return self, []

        mod_used = [False] * len(cost_mods)
        power, life = self.power, self.life
        for i, mod in enumerate(cost_mods):
            if power in mod.power_ittt:
                power = mod.power_ittt[power]
                mod_used[i] = True

        return (Cost(power=power, life=life, discard=self.discard,
                     own_ally=self.own_ally, any_ally=self.any_ally),
                [x for i, x in enumerate(cost_mod_srcs) if mod_used[i]])

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
