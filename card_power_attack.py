import sys

from card_power import CardPower
from cost import Cost
from damage import Damage


class CardPowerAttack(CardPower):
    def __init__(self, name, description, is_physical=None,
                 cost=None, damage=None, damage_modifier=None,
                 own_anger=None, opp_anger=None,
                 own_power=None, opp_power=None,
                 exhaust=True, discard=True, remove_from_game=False,
                 is_floating=None, card=None):
        if cost is None:
            cost = Cost.energy_attack() if (is_physical is False) else Cost.none()
        super().__init__(name, description, cost, card=card, is_floating=is_floating)

        if damage is None:
            if is_physical is None:
                damage = Damage.none()
            elif is_physical:
                damage = Damage.physical_attack()
            else:
                damage = Damage.energy_attack()
        if damage_modifier:
            damage.modify(damage_modifier)
        self.damage = damage

        self.is_physical = is_physical
        self.own_anger = own_anger
        self.opp_anger = opp_anger
        self.own_power = own_power
        self.opp_power = opp_power
        self.exhaust = exhaust
        self.discard = discard
        self.remove_from_game = remove_from_game

    def on_attack(self, player, phase):
        if self.is_physical is None:  # Non-combat attacks
            print(f'{player} uses {self}')
        else:
            print(f'{player} uses {self} for {self.damage}')

        player.pay_cost(self.cost)

        if self.own_anger is not None:
            player.adjust_anger(self.own_anger)
        if self.opp_anger is not None:
            player.opponent.adjust_anger(self.opp_anger)

        if self.own_power is not None:
            player.personality.adjust_power_stage(self.own_power)
        if self.opp_power is not None:
            player.opponent.personality.adjust_power_stage(self.opp_power)

        if self.is_physical is None:  # Non-combat attacks
            success = True
        elif self.is_physical:
            success = phase.physical_attack(self.damage, src=self)
        else:
            success = phase.energy_attack(self.damage, src=self)

        if success:
            self.on_success(player, phase)

        self.on_resolved(player, phase)

    def on_success(self, player, phase):
        pass

    def on_resolved(self, player, phase):
        # TODO: easy option for exhaust after this turn?
        if self.exhaust:
            if self.card:
                player.exhaust_card(card=self.card)
            else:
                player.exhaust_card_power(self)
        else:
            self.exhaust_until_next_turn()

        if self.card:
            if self.remove_from_game:
                player.remove_from_game(self.card, exhaust_card=False)
            elif self.discard:
                player.discard(self.card, exhaust_card=False)
            self.discard = self.remove_from_game = False


class CardPowerPhysicalAttack(CardPowerAttack):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, is_physical=True)


class CardPowerEnergyAttack(CardPowerAttack):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, is_physical=False)


class CardPowerNonCombatAttack(CardPowerAttack):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, is_physical=None)
