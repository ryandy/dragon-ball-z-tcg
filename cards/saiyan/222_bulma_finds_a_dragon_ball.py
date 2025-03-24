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


CARD_POWER = CardPowerBFADB(NAME, CARD_TEXT, remove_from_game=True,
                            cost=Cost(ally_in_play_req=Character.BULMA))
