import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Goku\'s Physical Attack'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '25'
RARITY = 1
DECK_LIMIT = 2
CHARACTER = 'Goku'
STYLE = None
CARD_TEXT = ('Physical attack. If successful, draw the bottom card from your discard pile. If used'
             ' by Goku, it stays in play to be used one more time this Combat. Remove from the'
             ' game after use.')


class CardPowerPhysicalAttackGPA(CardPowerPhysicalAttack):
    def on_success(self, player, phase):
        card = player.discard_pile.draw_from_bottom()
        if card:
            player.add_card_to_hand(card)

    def on_resolved(self):
        self.resolved_count += 1
        if self.resolved_count > 2:
            assert False
        elif self.resolved_count == 2:
            self.player.exhaust_card_power(self)
            return

        # First time through, if not Goku, exhaust/remove as normal
        if self.player.control_personality.character != Character.GOKU:
            super().on_resolved()
            return

        # Used by Goku, set up for second use
        self.exhaust_after_this_turn()
        if self.card:
            self.player.remove_from_game(self.card, exhaust_card=False)
        self.set_floating()


CARD_POWER = CardPowerPhysicalAttackGPA(NAME, CARD_TEXT, remove_from_game=True)
