import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Orange Off-Balancing Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '134'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Orange'
RESTRICTED = False
CARD_TEXT = ('Stop the first physical attack made on you in a combat.')


class CardPowerPhysicalDefenseOOBD(CardPowerPhysicalDefense):
    def is_restricted(self, player):
        if len([x for x in player.opponent.card_powers_played_this_combat
                if isinstance(x, CardPowerPhysicalAttack)]) > 1:
            return True
        return super().is_restricted(player)


CARD_POWER = CardPowerPhysicalDefenseOOBD(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False)
