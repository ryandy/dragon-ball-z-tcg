import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Gohan\'s Anger'
SAGA = 'Saiyan'
CARD_NUMBER = 'BK2'
RARITY = 2
DECK_LIMIT = None
CHARACTER = 'Gohan'
STYLE = None
CARD_TEXT = ('Raise your anger by 2 and reduce every villain\'s anger by 1.'
             ' Remove from the game after use.')


class CardPowerNonCombatAttackGA(CardPowerNonCombatAttack):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        if not player.opponent.main_personality.is_hero:
            player.opponent.adjust_anger(-1)


CARD_POWER = CardPowerNonCombatAttackGA(NAME, CARD_TEXT, own_anger=2, remove_from_game=True)
