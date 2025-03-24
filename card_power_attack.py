import copy
import sys

from card_power import CardPower
from cost import Cost
from damage import Damage
from dragon_ball_card import DragonBallCard
from state import State
from util import dprint


class CardPowerAttack(CardPower):
    def __init__(self, name, description, is_physical=None,
                 heroes_only=False, villains_only=False, saiyan_only=False, namekian_only=False,
                 cost=None, damage=None, damage_modifier=None,
                 own_anger=None, opp_anger=None,
                 own_power=None, opp_power=None,
                 end_combat=None,
                 exhaust=True, discard=True, remove_from_game=False,
                 is_floating=None, card=None):
        if cost is None:
            cost = Cost.energy_attack() if (is_physical is False) else Cost.none()
        super().__init__(name, description, cost,
                         heroes_only=heroes_only, villains_only=villains_only,
                         saiyan_only=saiyan_only, namekian_only=namekian_only,
                         card=card, is_floating=is_floating)

        if damage is None:
            if is_physical is None:
                damage = Damage.none()
            elif is_physical:
                damage = Damage.physical_attack()
            else:
                damage = Damage.energy_attack()
        damage = damage.copy()
        if damage_modifier:
            damage.modify(damage_modifier)
        self.damage = damage

        self.is_physical = is_physical
        self.own_anger = own_anger
        self.opp_anger = opp_anger
        self.own_power = own_power
        self.opp_power = opp_power
        self.end_combat = end_combat
        self.exhaust = exhaust
        self.discard = discard
        self.remove_from_game = remove_from_game

    def copy(self):
        # Note: do not deep copy self.card
        card_power_copy = copy.copy(self)
        card_power_copy.cost = self.cost.copy()
        card_power_copy.damage = self.damage.copy()
        return card_power_copy

    def on_attack(self, player, phase):
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

        if self.is_physical is None:  # Non-combat attacks
            success = True
        elif self.is_physical:
            success = phase.physical_attack(self.damage.copy())
        else:
            success = phase.energy_attack(self.damage.copy())

        if success:
            self.on_success(player, phase)

        if self.end_combat:
            phase.set_end_combat()

        self.on_resolved(player, phase)

    def on_success(self, player, phase):
        pass

    def on_resolved(self, player, phase):
        if self.exhaust:
            if self.card:
                player.exhaust_card(self.card)
            else:
                player.exhaust_card_power(self)
        else:
            if self.card:
                player.exhaust_card_until_next_turn(card=self.card)
            else:
                self.exhaust_until_next_turn()

        if self.card:
            if self.remove_from_game:
                player.remove_from_game(self.card, exhaust_card=False)
            elif self.discard:
                player.discard(self.card, exhaust_card=False)


class CardPowerPhysicalAttack(CardPowerAttack):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, is_physical=True)


class CardPowerEnergyAttack(CardPowerAttack):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, is_physical=False)


class CardPowerNonCombatAttack(CardPowerAttack):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, is_physical=None)


# Physical attack used by Piccolo and Tien personalities
class CardPowerMultiForm(CardPowerPhysicalAttack):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resolved_turn = -1
        self.resolved_count = 0

    def on_resolved(self, player, phase):
        # Reset each turn the power is used
        if self.resolved_turn != State.TURN:
            self.resolved_turn = State.TURN
            self.resolved_count = 0

        self.resolved_count += 1
        if self.resolved_count > 2:
            assert False
        elif self.resolved_count == 2:
            player.exhaust_card_until_next_turn(card=self.card)
        else:
            phase.set_skip_next_attack_phase()
            phase.set_next_attack_power(self)
