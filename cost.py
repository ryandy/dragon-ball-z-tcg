import copy
import sys

from character import Character


class Cost:
    def __init__(self, power=None, life=None,
                 discard=None,
                 own_ally=None):
        self.power = power or 0
        self.life = life or 0
        self.discard = discard or 0
        # TODO: not sure if this should be int/list/Character/Card...
        self.own_ally = own_ally or 0

    def copy(self):
        return copy.copy(self)

    def is_none(self):
        return (self.power == 0
                and self.life == 0
                and self.discard == 0
                and self.own_ally == 0)

    def can_afford(self, player, card_power):
        return (player.control_personality.power_stage >= self.power
                and len(player.life_deck) >= self.life
                and len([x for x in player.hand
                         if x is not card_power.card]) >= self.discard
                and len(player.allies) >= self.own_ally)

    def pay(self, player, card_power):
        assert self.can_afford(player, card_power)
        player.control_personality.reduce_power_stage(self.power)
        player.apply_life_damage(self.life)

        for _ in range(self.discard):
            card = player.choose_hand_discard_card(ignore_card=card_power.card)
            player.discard(card)

        for _ in range(self.own_ally):
            ally = player.choose_personality(
                skip_main=True, prompt='Select an ally to sacrifice')
            # TODO: assuming remove from game for now
            player.remove_from_game(ally)

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
