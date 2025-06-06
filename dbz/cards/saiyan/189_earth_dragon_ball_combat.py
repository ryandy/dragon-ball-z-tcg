import sys

from dbz.card_power_attack import CardPowerEnergyAttack
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


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
