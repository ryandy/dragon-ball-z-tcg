import sys

from card_power_attack import CardPowerEnergyAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Earth Dragon Ball Combat'
SUBTYPE = 'Energy Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '189'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Energy attack. If successful, capture a Dragon Ball.')


class CardPowerEnergyAttackEDBC(CardPowerEnergyAttack):
    def on_success(self, player, phase):
        player.steal_dragon_ball()


CARD_POWER = CardPowerEnergyAttackEDBC(NAME, CARD_TEXT)
