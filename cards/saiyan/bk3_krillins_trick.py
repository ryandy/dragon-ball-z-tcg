import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Krillin\'s Trick'
SAGA = 'Saiyan'
CARD_NUMBER = 'BK3'
RARITY = 2
DECK_LIMIT = None
CHARACTER = 'Krillin'
STYLE = None
CARD_TEXT = ('Steal a Dragon Ball. Remove from the game after use.')


class CardPowerNonCombatAttackKT(CardPowerNonCombatAttack):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        player.steal_dragon_ball()


CARD_POWER = CardPowerNonCombatAttackKT(NAME, CARD_TEXT, remove_from_game=True)
