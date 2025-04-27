import copy
import sys

from card_power import CardPower
from cost import Cost
from damage_modifier import DamageModifier
from util import dprint


class CardPowerDefense(CardPower):
    def __init__(self, name, description, is_physical=None,
                 heroes_only=False, villains_only=False, saiyan_only=False, namekian_only=False,
                 cost=None, damage_modifier=None,
                 rejuvenate_count=None, rejuvenate_choice_count=None,
                 own_anger=None, opp_anger=None,
                 main_power=None, any_power=None, opp_power=None,
                 exhaust=True, exhaust_until_next_turn=False,
                 discard=True, remove_from_game=False,
                 is_floating=None, card=None):
        super().__init__(name, description, cost or Cost.none(),
                         exhaust=exhaust, exhaust_until_next_turn=exhaust_until_next_turn,
                         discard=discard, remove_from_game=remove_from_game,
                         heroes_only=heroes_only, villains_only=villains_only,
                         saiyan_only=saiyan_only, namekian_only=namekian_only,
                         card=card, is_floating=is_floating)
        self.is_physical = is_physical
        self.damage_modifier = damage_modifier.copy() if damage_modifier else None
        self.rejuvenate_count = rejuvenate_count
        self.rejuvenate_choice_count = rejuvenate_choice_count
        self.own_anger = own_anger
        self.opp_anger = opp_anger
        self.main_power = main_power
        self.any_power = any_power
        self.opp_power = opp_power

    def copy(self):
        # Note: do not deep copy self.card
        card_power_copy = copy.copy(self)
        card_power_copy.cost = self.cost.copy()
        card_power_copy.damage_modifier = (
            self.damage_modifier.copy() if self.damage_modifier else None)
        return card_power_copy

    def on_defense(self, player, phase, damage):
        self.on_pay_cost(player, phase)

        self.on_secondary_effects(player, phase)

        damage_modifier = self.damage_modifier or DamageModifier(stopped=True)
        damage.modify(damage_modifier)

        self.on_resolved()
        return damage

    def on_pay_cost(self, player, phase):
        self.cost.pay(player, self)

    def on_secondary_effects(self, player, phase):
        if self.own_anger:
            player.adjust_anger(self.own_anger)
        if self.opp_anger:
            player.opponent.adjust_anger(self.opp_anger)

        if self.main_power:
            player.main_personality.adjust_power_stage(self.main_power)
        if self.any_power:
            personality = player.choose_power_stage_target(self.any_power)
            personality.adjust_power_stage(self.any_power)
        if self.opp_power:
            player.opponent.main_personality.adjust_power_stage(self.opp_power)

        if self.rejuvenate_count:
            for _ in range(self.rejuvenate_count):
                player.rejuvenate()

        if self.rejuvenate_choice_count:
            for _ in range(self.rejuvenate_choice_count):
                player.rejuvenate_with_choice()


class CardPowerPhysicalDefense(CardPowerDefense):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, is_physical=True)


class CardPowerEnergyDefense(CardPowerDefense):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, is_physical=False)


class CardPowerAnyDefense(CardPowerDefense):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, is_physical=None)
