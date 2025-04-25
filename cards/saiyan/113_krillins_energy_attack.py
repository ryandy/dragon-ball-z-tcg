import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Krillin\'s Energy Attack'
SUBTYPE = 'Energy Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '113'
RARITY = 3
DECK_LIMIT = None
CHARACTER = 'Krillin'
STYLE = None
CARD_TEXT = ('Energy attack doing 2 life cards of damage. If used by Krillin, it stays in play'
             ' to be used one more time this combat.')


class CardPowerEnergyAttackKEA(CardPowerEnergyAttack):
    def on_resolved(self, player, phase):
        self.resolved_count += 1
        if self.resolved_count > 2:
            assert False
        elif self.resolved_count == 2:
            player.exhaust_card_power(self)
            return

        # First time through, if not Krillin, exhaust/remove as normal
        if player.control_personality.character != Character.KRILLIN:
            super().on_resolved(player, phase)
            return

        # Used by Krillin, set up for second use
        self.exhaust_after_this_turn()
        if self.card:
            player.remove_from_game(self.card, exhaust_card=False)
        self.set_floating()


CARD_POWER = CardPowerEnergyAttackKEA(NAME, CARD_TEXT, damage=Damage(life=2))
