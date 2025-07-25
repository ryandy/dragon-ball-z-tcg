import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Goku\'s Energy Defense'
SUBTYPE = 'Energy Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '108'
RARITY = 3
DECK_LIMIT = None
CHARACTER = 'Goku'
STYLE = None
CARD_TEXT = ('Prevents 3 life cards from being discarded from a successful energy attack. If used'
             ' by Goku, it stays on the table to be used one more time in this combat.')


class CardPowerEnergyDefenseGED(CardPowerEnergyDefense):
    def on_resolved(self):
        self.resolved_count += 1
        if self.resolved_count > 2:
            assert False
        elif self.resolved_count == 2:
            self.player.exhaust_card_power(self)
            return

        # First time through, if not Goku, exhaust/remove as normal
        if self.player.character != Character.GOKU:
            super().on_resolved()
            return

        # Used by Goku, set up for second use
        self.exhaust_after_this_turn()
        if self.card:
            self.player.discard(self.card, exhaust_card=False)
        self.set_floating()


CARD_POWER = CardPowerEnergyDefenseGED(
    NAME, CARD_TEXT, damage_modifier=DamageModifier(life_prevent=3))
