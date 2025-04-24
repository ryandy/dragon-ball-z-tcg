import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerNonCombatAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerAnyDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Vegeta\'s Energy Blast'
SUBTYPE = 'Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '119'
RARITY = 3
DECK_LIMIT = None
CHARACTER = 'Vegeta'
STYLE = None
CARD_TEXT = ('Saiyan Heritage only. Use when needed. This must be your first card played'
             ' during Combat. Raise your Main Personality to its highest power stage.'
             ' Remove from the game after use.')


# Note: player.cards_played_this_combat currently tracks cards associated with CardPowerAttack,
#       CardPowerDefense, and CardPowerDefenseShield. Are there other CardPower types to check?
class CardPowerNonCombatAttackVEB(CardPowerNonCombatAttack):
     def is_restricted(self, player):
         if len(player.cards_played_this_combat) > 0:
             return True
         return super().is_restricted(player)


class CardPowerAnyDefenseVEB(CardPowerAnyDefense):
     def is_restricted(self, player):
         if len(player.cards_played_this_combat) > 0:
             return True
         return super().is_restricted(player)


CARD_POWER = [
    CardPowerNonCombatAttackVEB(
        NAME, CARD_TEXT, main_power=10, saiyan_only=True, remove_from_game=True),
    CardPowerAnyDefenseVEB(
        NAME, CARD_TEXT, main_power=10, saiyan_only=True, remove_from_game=True)
]
