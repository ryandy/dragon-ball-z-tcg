import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Frieza\'s Spirit'
SAGA = 'Saiyan'
CARD_NUMBER = 'BK5'
RARITY = 2
DECK_LIMIT = None
CHARACTER = 'Frieza'
STYLE = None
CARD_TEXT = ('You reduce every hero\'s anger level to zero. Remove from the game after use.')


class CardPowerNonCombatAttackFS(CardPowerNonCombatAttack):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        if player.opponent.main_personality.is_hero:
            player.opponent.adjust_anger(-5)


CARD_POWER = CardPowerNonCombatAttackFS(NAME, CARD_TEXT, remove_from_game=True)
