import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Blue Enemies Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '141'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Blue'
RESTRICTED = False
CARD_TEXT = ('Once per Combat, if your opponent has an Ally in play, you may prevent'
             ' 1 life card of damage from any physical attack.')


class CardPowerPhysicalDefenseBED(CardPowerPhysicalDefense):
    def is_restricted(self, player):
        if len(player.opponent.allies) == 0:
            return True
        return super().is_restricted(player)


CARD_POWER = CardPowerPhysicalDefenseBED(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
    damage_modifier=DamageModifier(life_prevent=1))
