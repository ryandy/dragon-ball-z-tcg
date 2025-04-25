import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerAnyDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Krillin\'s Physical Defense'
SUBTYPE = 'Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '112'
RARITY = 3
DECK_LIMIT = None
CHARACTER = 'Krillin'
STYLE = None
CARD_TEXT = ('Play this card as a defense. If your opponent’s attack does life cards of damage'
             ' to you, you may take the first life card of damage from that attack and place it'
             ' in your hand instead of discarding it. If used by Krillin, this card stays in play'
             ' to be used one more time this Combat.')


class CardPowerAnyDefenseKPD(CardPowerAnyDefense):
    def on_resolved(self, player, phase):
        self.resolved_count += 1
        if self.resolved_count > 2:
            assert False
        elif self.resolved_count == 2:
            player.exhaust_card_power(self)
            return

        # First time through, if not Krillin, exhaust/discard as normal
        if player.control_personality.character != Character.KRILLIN:
            super().on_resolved(player, phase)
            return

        # Used by Krillin, set up for second use
        self.exhaust_after_this_turn()
        if self.card:
            player.discard(self.card, exhaust_card=False)
        self.set_floating()


CARD_POWER = CardPowerAnyDefenseKPD(
    NAME, CARD_TEXT, damage_modifier=DamageModifier(life_prevent_and_draw=1))
