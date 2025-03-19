import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Roshi Training'
SAGA = 'Saiyan'
CARD_NUMBER = '78'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Heroes only. The top 3 discarded cards are placed at the bottom of your life deck.')


class CardPowerRT(CardPowerNonCombatAttack):
    def on_success(self, player, phase):
        for _ in range(3):
            player.rejuvenate()


CARD_POWER = CardPowerRT(NAME, CARD_TEXT, heroes_only=True)
