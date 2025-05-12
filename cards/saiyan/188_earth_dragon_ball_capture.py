import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Earth Dragon Ball Capture'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '188'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Capture an opponent\'s Dragon Ball.')


class CardPowerNonCombatAttackEDBC(CardPowerNonCombatAttack):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        player.steal_dragon_ball()


CARD_POWER = CardPowerNonCombatAttack(NAME, CARD_TEXT)
