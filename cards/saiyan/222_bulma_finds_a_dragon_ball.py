import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Bulma Finds a Dragon Ball'
SAGA = 'Saiyan'
CARD_NUMBER = '222'
RARITY = 5
DECK_LIMIT = None
CHARACTER = 'Bulma'
STYLE = None
CARD_TEXT = ('When the Bulma ally is in play, use this card to capture a Dragon Ball. Remove from'
             ' the game after use.')


class CardPowerBFADB(CardPowerNonCombatAttack):
    def on_success(self, player, phase):
        player.steal_dragon_ball()

    def is_restricted(self, player):
        allies_in_play = [x for x in player.allies + player.opponent.allies]
        if not any(x.character == Character.BULMA for x in allies_in_play):
            return True
        return super().is_restricted(player)


CARD_POWER = CardPowerBFADB(NAME, CARD_TEXT, remove_from_game=True)
