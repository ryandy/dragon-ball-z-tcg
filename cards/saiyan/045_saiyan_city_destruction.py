import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Saiyan City Destruction'
SAGA = 'Saiyan'
CARD_NUMBER = '45'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Saiyan'
CARD_TEXT = ('Villains only. Skip your next Combat step. Place the top 2 cards from your discard'
             ' pile on the bottom of your Life Deck. Remove from the game after use.')


class CardPowerSCD(CardPowerNonCombatAttack):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        player.must_skip_next_combat = True


CARD_POWER = CardPowerSCD(
    NAME, CARD_TEXT, villains_only=True, rejuvenate_count=2, remove_from_game=True)
