import copy
import sys

from card_power import CardPower
from cost import Cost


class CardPowerOnDraw(CardPower):
    def __init__(self, name, description,
                 own_attack_draw_add=None, own_defend_draw_add=None,
                 opp_attack_draw_add=None, opp_defend_draw_add=None,
                 own_attack_draw_from_discard_add=None,
                 own_defend_draw_from_discard_add=None,
                 choice=False, exhaust=True, discard=True, remove_from_game=False):
        super().__init__(name, description, Cost.none())
        self.own_attack_draw_add = own_attack_draw_add or 0
        self.own_defend_draw_add = own_defend_draw_add or 0
        self.opp_attack_draw_add = opp_attack_draw_add or 0
        self.opp_defend_draw_add = opp_defend_draw_add or 0
        self.own_attack_draw_from_discard_add = own_attack_draw_from_discard_add or 0
        self.own_defend_draw_from_discard_add = own_defend_draw_from_discard_add or 0
        self.choice = choice
        self.exhaust = exhaust
        self.discard = discard
        self.remove_from_game = remove_from_game

    def copy(self):
        # Note: do not deep copy self.card
        return copy.copy(self)

    def on_draw(self, phase):
        activated = (
            # Own draw phase, attacking
            ((self.own_attack_draw_add or self.own_attack_draw_from_discard_add)
             and self.player is phase.player and phase.is_attacker)
            or  # Own draw phase, defending
            ((self.own_defend_draw_add or self.own_defend_draw_from_discard_add)
             and self.player is phase.player and not phase.is_attacker)
            or  # Opp draw phase, they are attacking
            (self.opp_attack_draw_add
             and self.player is not phase.player and phase.is_attacker)
            or  # Opp draw phase, they are defending
            (self.opp_defend_draw_add
             and self.player is not phase.player and not phase.is_attacker)
        )

        if (activated
            and (not self.choice or self.player.choose_to_use_card_power(self))):
            self.on_activated(phase)
            self.on_resolved(phase)

    def on_activated(self, phase):
        phase.draw_count += self.own_attack_draw_add
        phase.discard_pile_draw_count += self.own_attack_draw_from_discard_add
        phase.draw_count += self.own_defend_draw_add
        phase.discard_pile_draw_count += self.own_defend_draw_from_discard_add
        phase.draw_count += self.opp_attack_draw_add
        phase.draw_count += self.opp_defend_draw_add

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
