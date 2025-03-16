import sys

from combat_card import CombatCard
from draw_phase import DrawPhase
from phase import Phase


class CombatPhase(Phase):
    def __init__(self, player):
        self.player = player
        self.passed = True

    def execute(self):
        # TODO give player opportunity to pass
        self.passed = False

        opp_draw_phase = DrawPhase(self.player.opponent)
        opp_draw_phase.execute()

        card = self.player.hand.cards[0]
        if (isinstance(card, CombatCard) and card.is_attack and card.is_physical
            and card.card_power_condition(card, self.player, self)):
            card.card_power(card, self.player, self)

    def physical_attack(self, attack_damage=None, from_card=None):
        if attack_damage is None:
            attack_idx = self.player.personality.get_physical_attack_table_index()
            defend_idx = self.player.opponent.personality.get_physical_attack_table_index()
            attack_damage = max(0, 1 + attack_idx - defend_idx)
        if from_card and True:
            print(f'{self.player} uses {from_card} for {attack_damage} damage')
        self.player.opponent.apply_physical_damage(attack_damage)
