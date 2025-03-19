import sys

from card_power import CardPower
from cost import Cost
from damage import Damage


class CardPowerAttack(CardPower):
    def __init__(self, name, description, is_physical=True,
                 cost=None, damage=None, damage_modifier=None,
                 own_anger=None, opp_anger=None,
                 exhaust=True, discard=True, remove_from_game=None,
                 is_floating=None, card=None):
        if cost is None:
            cost = Cost.none() if is_physical else Cost.energy_attack()
        super().__init__(name, description, cost, card=card, is_floating=is_floating)

        if damage is None:
            damage = Damage.physical_attack() if is_physical else Damage.energy_attack()
        if damage_modifier:
            damage.modify(damage_modifier)
        self.damage = damage

        self.is_physical = is_physical
        self.own_anger = own_anger
        self.opp_anger = opp_anger
        self.exhaust = exhaust
        self.discard = discard
        self.remove_from_game = remove_from_game

    def on_attack(self, player, phase):
        player.pay_cost(self.cost)

        if self.own_anger is not None:
            player.adjust_anger(self.own_anger)
        if self.opp_anger is not None:
            player.opponent.adjust_anger(self.opp_anger)

        if self.is_physical:
            success = phase.physical_attack(self.damage, src=self.name)
        else:
            success = phase.energy_attack(self.damage, src=self.name)

        if success:
            self.on_success(player, phase)

        self.on_resolved(player, phase)

    def on_success(self, player, phase):
        pass

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
