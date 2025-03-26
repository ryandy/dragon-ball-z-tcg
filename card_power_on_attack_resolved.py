import copy
import sys

from card_power import CardPower
from cost import Cost


class CardPowerOnAttackResolved(CardPower):
    def __init__(self, name, description,
                 choice=False, exhaust=True, discard=True, remove_from_game=False):
        super().__init__(name, description, Cost.none())
        self.choice = choice
        self.exhaust = exhaust
        self.discard = discard
        self.remove_from_game = remove_from_game

    def copy(self):
        # Note: do not deep copy self.card
        return copy.copy(self)

    def on_attack_resolved(self, phase, damage, is_physical):
        if (self.on_condition(phase, damage, is_physical)
            and (not self.choice or self.player.choose_to_use_card_power(self))):
            self.on_effect(phase, damage, is_physical)
            self.on_resolved(phase)

    def on_condition(self, phase, damage, is_physical):
        return True

    def on_effect(self, phase, damage, is_physical):
        pass

    def on_resolved(self, phase):
        if self.exhaust:
            if self.card:
                self.player.exhaust_card(self.card)
            else:
                self.player.exhaust_card_power(self)

        if self.card:
            if self.remove_from_game:
                self.player.remove_from_game(self.card, exhaust_card=False)
            elif self.discard:
                self.player.discard(self.card, exhaust_card=False)
