import sys

from card_power_attack import CardPowerNonCombatAttack
from card_power_dragon_ball import CardPowerDragonBall
from character import Character
from combat_attack_phase import CombatAttackPhase
from combat_defense_phase import CombatDefensePhase
from combat_phase import CombatPhase
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier
from util import dprint


TYPE = 'Dragon Ball'
NAME = 'Earth Dragon Ball 7'
DB_SET = 'Earth'
DB_NUMBER = 7
SAGA = 'Saiyan'
CARD_NUMBER = '187'
RARITY = 5
DECK_LIMIT = 1
CHARACTER = None
STYLE = None
CARD_TEXT = ('Play this card during combat to end the battle. Pick 3 cards out of your discard'
             ' pile and place them at the top of your life deck. All opponents\' anger levels'
             ' shift down 2.')


# Two card powers:
#   - dragon ball power that just does the basic stuff if played during non-combat
#   - attack power that also ends combat
#     - card power registered when drawn
#     - card power needs to be exhausted if/when played during non-combat


def _search_discard_pile(player):
    for _ in range(3):
        card = player.choose_discard_pile_card()
        if card:
            dprint(f'{player} returns {card} to their life deck')
            player.discard_pile.remove(card)
            player.life_deck.add_top(card)
            card.set_pile(player.life_deck)


class CardPowerDragonBallEDB7(CardPowerDragonBall):
    def on_play(self, player, phase):
        player.opponent.adjust_anger(-2)
        _search_discard_pile(player)

        # In special circumstances can be played during CombatPhase not as a CardPowerAttack
        # e.g. another card searches deck for a dragon ball and plays it during combat
        if (isinstance(phase, CombatPhase)
            or isinstance(phase, CombatAttackPhase)
            or isinstance(phase, CombatDefensePhase)):
            phase.set_force_end_combat()

        # Need to exhaust the registered attack card power
        player.exhaust_card_by_id('saiyan.187')  # Earth Dragon Ball 7


class CardPowerNonCombatAttackEDB7(CardPowerNonCombatAttack):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        _search_discard_pile(player)

    def on_resolved(self):
        super().on_resolved()

        # Card is played from hand so must be put into DB area
        if self.card:
            assert self.card.pile is self.player.hand
            self.player.hand.remove(self.card)
            self.player.dragon_balls.add(self.card)
            self.card.set_pile(self.player.dragon_balls)


CARD_POWER = [
    CardPowerDragonBallEDB7(NAME, CARD_TEXT),
    CardPowerNonCombatAttackEDB7(
        NAME, CARD_TEXT, opp_anger=-2, discard=False, force_end_combat=True)
]
