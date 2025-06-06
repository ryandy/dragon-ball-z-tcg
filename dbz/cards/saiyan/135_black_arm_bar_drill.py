import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Black Arm Bar Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '135'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Black'
RESTRICTED = 'Orange'
CARD_TEXT = ('Stop the first energy attack made on you in a combat. Can\'t be used with any'
             ' other Orange drills in play.')


class CardPowerEnergyDefenseBABD(CardPowerEnergyDefense):
    def is_restricted(self, player):
        if len([x for x in player.opponent.card_powers_played_this_combat
                if isinstance(x, CardPowerEnergyAttack)]) > 1:
            return True
        return super().is_restricted(player)


CARD_POWER = CardPowerEnergyDefenseBABD(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False)
