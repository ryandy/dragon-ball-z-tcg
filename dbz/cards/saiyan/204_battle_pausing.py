import sys

from card_power_defense import CardPowerEnergyDefense, CardPowerAnyDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Battle Pausing'
SUBTYPE = 'Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '204'
RARITY = 5
DECK_LIMIT = 1
CHARACTER = None
STYLE = None
CARD_TEXT = ('Draw the top 2 cards from your discard pile. Your opponent’s Main Personality'
             ' gains 5 power stages. Remove from the game after use.')


class CardPowerAnyDefenseBP(CardPowerAnyDefense):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)

        # Draw 2 from the discard pile
        for _ in range(2):
            if len(player.discard_pile) > 0:
                card = player.discard_pile.draw()
                player.draw(card=card)


CARD_POWER = CardPowerAnyDefenseBP(
    NAME, CARD_TEXT, opp_power=5, remove_from_game=True,
    damage_modifier=DamageModifier.none())
