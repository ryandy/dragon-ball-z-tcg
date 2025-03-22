import copy
import sys

from card_power import CardPower
from cost import Cost
from damage_modifier import DamageModifier
from util import dprint


class CardPowerDefense(CardPower):
    def __init__(self, name, description, is_physical=True,
                 cost=None, damage_modifier=None,
                 own_anger=None, opp_anger=None,
                 exhaust=True, discard=True, remove_from_game=None,
                 is_floating=None, card=None):
        super().__init__(name, description, cost or Cost.none(), card=card, is_floating=is_floating)
        self.is_physical = is_physical
        self.damage_modifier = damage_modifier.copy() if damage_modifier else None
        self.own_anger = own_anger
        self.opp_anger = opp_anger
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
        player.pay_cost(self.cost)

        if self.own_anger is not None:
            player.adjust_anger(self.own_anger)
        if self.opp_anger is not None:
            player.opponent.adjust_anger(self.opp_anger)

        damage_modifier = self.damage_modifier or DamageModifier(stopped=True)
        damage.modify(damage_modifier)

        if damage.was_stopped():
            dprint(f'{player.name()} uses {self} to stop the attack')
        else:
            dprint(f'{player.name()} uses {src} to reduce damage')
        if not player.interactive:
            dprint(f'  - {self.description}')

        self.on_resolved(player, phase)
        return damage

    def on_resolved(self, player, phase):
        if self.exhaust:
            if self.card:
                player.exhaust_card(card=self.card)
            else:
                player.exhaust_card_power(self)
        else:
            self.exhaust_until_next_turn()

        if self.card:
            if self.remove_from_game:
                player.remove_from_game(self.card)
            elif self.discard:
                player.discard(self.card)
            self.discard = self.remove_from_game = False


class CardPowerPhysicalDefense(CardPowerDefense):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, is_physical=True)


class CardPowerEnergyDefense(CardPowerDefense):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, is_physical=False)
