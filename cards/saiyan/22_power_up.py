import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Power Up!'
SAGA = 'Saiyan'
CARD_NUMBER = '22'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Powers up 5 stages for a personality. Take the top discarded card and place at the'
             ' bottom of your life deck.')


class CardPowerPU(CardPowerNonCombatAttack):
    def on_success(self, player, phase):
        player.rejuvenate()


# TODO: Choose target personality for power stages
CARD_POWER = CardPowerPU(NAME, CARD_TEXT, own_power=5)
