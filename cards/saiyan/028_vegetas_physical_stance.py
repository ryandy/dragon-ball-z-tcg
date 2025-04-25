import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Vegeta\'s Physical Stance'
SUBTYPE = 'Physical Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '28'
RARITY = 1
DECK_LIMIT = 1
CHARACTER = 'Vegeta'
STYLE = None
CARD_TEXT = ('Stops a physical attack. Stops all physical attacks performed against you for the'
             ' remainder of Combat. Remove from the game after use.')


class CardPowerVPS(CardPowerPhysicalDefense):
    def on_resolved(self, player, phase):
        self.resolved_count += 1
        if self.resolved_count == 1:
            self.exhaust_after_this_turn()
            if self.card:
                player.remove_from_game(self.card, exhaust_card=False)
            self.set_floating()


CARD_POWER = CardPowerVPS(NAME, CARD_TEXT, remove_from_game=True)
