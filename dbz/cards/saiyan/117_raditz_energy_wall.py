import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerNonCombatAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerAnyDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Raditz Energy Wall'
SUBTYPE = 'Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '117'
RARITY = 3
DECK_LIMIT = None
CHARACTER = 'Raditz'
STYLE = None
CARD_TEXT = ('Forces a Hero opponent in this combat to discard 1 life card from their deck.'
             ' Remove from the game after use.')


class CardPowerNonCombatAttackREW(CardPowerNonCombatAttack):
     def is_restricted(self, player):
         if not player.opponent.main_personality.is_hero:
             return True
         return super().is_restricted(player)

     # Unblockable 1 life damage
     def on_secondary_effects(self, player, phase):
         super().on_secondary_effects(player, phase)
         player.opponent.apply_life_damage(1)


CARD_POWER = CardPowerNonCombatAttackREW(NAME, CARD_TEXT, remove_from_game=True)
