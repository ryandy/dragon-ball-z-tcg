import copy
import sys

from dbz.card_power import CardPower
from dbz.cost import Cost
from dbz.util import dprint


class CardPowerOnDraw(CardPower):
    def __init__(self, name, description,
                 own_attack_draw_add=None, own_defend_draw_add=None,
                 opp_attack_draw_add=None, opp_defend_draw_add=None,
                 own_attack_draw_from_discard_add=None,
                 own_defend_draw_from_discard_add=None,
                 own_attack_draw_from_discard_bottom_add=None,
                 own_defend_draw_from_discard_bottom_add=None,
                 choice=False, exhaust=True, discard=True, remove_from_game=False):
        super().__init__(name, description, Cost.none(),
                         exhaust=exhaust, discard=discard, remove_from_game=remove_from_game)
        self.own_attack_draw_add = own_attack_draw_add or 0
        self.own_defend_draw_add = own_defend_draw_add or 0
        self.opp_attack_draw_add = opp_attack_draw_add or 0
        self.opp_defend_draw_add = opp_defend_draw_add or 0
        self.own_attack_draw_from_discard_add = own_attack_draw_from_discard_add or 0
        self.own_defend_draw_from_discard_add = own_defend_draw_from_discard_add or 0
        self.own_attack_draw_from_discard_bottom_add = own_attack_draw_from_discard_bottom_add or 0
        self.own_defend_draw_from_discard_bottom_add = own_defend_draw_from_discard_bottom_add or 0
        self.choice = choice

    def copy(self):
        # Note: do not deep copy self.card
        return copy.copy(self)

    def on_draw(self, phase):
        activated = (
            # Own draw phase, attacking
            ((self.own_attack_draw_add
              or self.own_attack_draw_from_discard_add
              or self.own_attack_draw_from_discard_bottom_add)
             and self.player is phase.player and phase.is_attacker)
            or  # Own draw phase, defending
            ((self.own_defend_draw_add
              or self.own_defend_draw_from_discard_add
              or self.own_defend_draw_from_discard_bottom_add)
             and self.player is phase.player and not phase.is_attacker)
            or  # Opp draw phase, they are attacking
            (self.opp_attack_draw_add
             and self.player is not phase.player and phase.is_attacker)
            or  # Opp draw phase, they are defending
            (self.opp_defend_draw_add
             and self.player is not phase.player and not phase.is_attacker)
        )

        if (activated
            and self.on_condition(phase)
            and (not self.choice or self.player.choose_to_use_card_power(self))):
            dprint(f'{self.player} uses {self}')
            dprint(f'  - {self.description}')
            self.on_effect(phase)
            self.on_resolved()

    def on_condition(self, phase):
        return True

    def on_effect(self, phase):
        if self.player is phase.player and phase.is_attacker:
            phase.draw_count += self.own_attack_draw_add
            phase.discard_pile_draw_count += self.own_attack_draw_from_discard_add
            phase.discard_pile_bottom_draw_count += self.own_attack_draw_from_discard_bottom_add
        elif self.player is phase.player and not phase.is_attacker:
            phase.draw_count += self.own_defend_draw_add
            phase.discard_pile_draw_count += self.own_defend_draw_from_discard_add
            phase.discard_pile_bottom_draw_count += self.own_defend_draw_from_discard_bottom_add
        elif self.player is not phase.player and phase.is_attacker:
            phase.draw_count += self.opp_attack_draw_add
        elif self.player is not phase.player and not phase.is_attacker:
            phase.draw_count += self.opp_defend_draw_add
