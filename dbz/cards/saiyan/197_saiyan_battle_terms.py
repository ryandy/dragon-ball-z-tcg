import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier
from dbz.drill_card import DrillCard


TYPE = 'Non-Combat'
NAME = 'Saiyan Battle Terms'
SAGA = 'Saiyan'
CARD_NUMBER = '197'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Saiyan'
CARD_TEXT = ('Remove a Non-Combat Card or Ally from in front of another player from the game.'
             ' Remove from the game after use.')


class CardPowerNonCombatAttackSBT(CardPowerNonCombatAttack):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)

        # Interpreting this as allowing drills to be removed, but not Dragon Balls
        cards = (self.player.opponent.non_combat.cards
                 + self.player.opponent.drills.cards
                 + self.player.opponent.allies.cards)
        cards = [c for c in cards
                 if not isinstance(c, DrillCard) or c.can_be_removed(player.opponent)]
        if cards:
            idx = self.player.choose([str(c) for c in cards],
                                     [c.card_text for c in cards],
                                     allow_pass=False,
                                     prompt='Select an opponent card to remove from the game')
            card = cards[idx]
            self.player.opponent.remove_from_game(card)


CARD_POWER = CardPowerNonCombatAttackSBT(NAME, CARD_TEXT, remove_from_game=True)
