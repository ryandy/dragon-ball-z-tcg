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


class CardPowerNonCombatAttackBFADB(CardPowerNonCombatAttack):
    def is_restricted(self, player):
        if not player.character_in_play(Character.BULMA, either_side=True, skip_main=True):
            return True
        if not player.can_steal_dragon_ball():
            return True
        return super().is_restricted(player)

    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        player.steal_dragon_ball()


CARD_POWER = CardPowerNonCombatAttackBFADB(NAME, CARD_TEXT, remove_from_game=True)
