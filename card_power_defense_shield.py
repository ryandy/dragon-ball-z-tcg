import copy
import sys

from card_power import CardPower
from cost import Cost
from damage_modifier import DamageModifier
from util import dprint


class CardPowerDefenseShield(CardPower):
    def __init__(self, name, description, is_physical=None,
                 cost=None, damage_modifier=None,
                 own_anger=None, opp_anger=None,
                 own_power=None, opp_power=None,
                 exhaust=True, discard=True, remove_from_game=None,
                 is_floating=None, card=None):
        super().__init__(name, description, cost or Cost.none(), card=card, is_floating=is_floating)
        self.is_physical = is_physical
        self.damage_modifier = damage_modifier.copy() if damage_modifier else None
        self.own_anger = own_anger
        self.opp_anger = opp_anger
        self.own_power = own_power
        self.opp_power = opp_power
        self.exhaust = exhaust
        self.discard = discard
        self.remove_from_game = remove_from_game

    def copy(self):
        # Note: do not deep copy self.card
        card_power_copy = copy.copy(self)
        card_power_copy.cost = self.cost.copy()
        card_power_copy.damage_modifier = (
            self.damage_modifier.copy() if self.damage_modifier else None)
        return card_power_copy

    def on_defense(self, player, phase, damage):
        self.cost.pay(player)

        if self.own_anger is not None:
            player.adjust_anger(self.own_anger)
        if self.opp_anger is not None:
            player.opponent.adjust_anger(self.opp_anger)

        if self.own_power is not None:
            player.personality.adjust_power_stage(self.own_power)
        if self.opp_power is not None:
            assert False  # Feels like this shouldn't be possible
            player.opponent.personality.adjust_power_stage(self.opp_power)

        damage_modifier = self.damage_modifier or DamageModifier(stopped=True)
        damage.modify(damage_modifier)

        self.on_resolved(player, phase)
        return damage

    def on_resolved(self, player, phase):
        if self.exhaust:
            if self.card:
                player.exhaust_card(card=self.card)
            else:
                player.exhaust_card_power(self)
        else:
            if self.card:
                player.exhaust_card_until_next_turn(card=self.card)
            else:
                self.exhaust_until_next_turn()

        if self.card:
            if self.remove_from_game:
                player.remove_from_game(self.card)
            elif self.discard:
                player.discard(self.card)


class CardPowerPhysicalDefenseShield(CardPowerDefenseShield):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, is_physical=True)


class CardPowerEnergyDefenseShield(CardPowerDefenseShield):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, is_physical=False)


class CardPowerAnyDefenseShield(CardPowerDefenseShield):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, is_physical=None)
