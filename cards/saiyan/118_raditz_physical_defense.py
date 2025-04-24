import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerNonCombatAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerAnyDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Raditz Physical Defense'
SUBTYPE = 'Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '118'
RARITY = 3
DECK_LIMIT = None
CHARACTER = 'Raditz'
STYLE = None
CARD_TEXT = ('Forces a Hero opponent in this combat to take their anger level down 2.'
             ' Remove from the game after use.')


class CardPowerNonCombatAttackRPD(CardPowerNonCombatAttack):
     def is_restricted(self, player):
         # Checking main rather than control because anger is only relevant for main
         if not player.opponent.main_personality.is_hero:
             return True
         return super().is_restricted(player)


CARD_POWER = CardPowerNonCombatAttackRPD(NAME, CARD_TEXT, opp_anger=-2, remove_from_game=True)
