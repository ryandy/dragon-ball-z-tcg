import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


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


class CardPowerGED(CardPowerEnergyDefense):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resolved_count = 0

    def on_resolved(self, player, phase):
        if player.character != Character.GOKU:
            return super().on_resolved(player, phase)

        self.resolved_count += 1
        if self.resolved_count > 2:
            assert False
        elif self.resolved_count == 2:
            player.exhaust_card_power(self)
        else:
            self.exhaust_after_this_turn()
            player.discard(self.card, exhaust_card=False)
            self.set_floating()


CARD_POWER = CardPowerGED(NAME, CARD_TEXT, damage_modifier=DamageModifier(life_prevent=3))
