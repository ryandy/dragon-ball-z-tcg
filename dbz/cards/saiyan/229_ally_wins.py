import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerNonCombatAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerAnyDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Ally Wins!'
SUBTYPE = 'Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '229'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Your opponent discards one life card for every Ally you have in play.'
             ' Remove from the game after use.')


class CardPowerNonCombatAttackAW(CardPowerNonCombatAttack):
     # Unblockable life damage
     def on_secondary_effects(self, player, phase):
         super().on_secondary_effects(player, phase)
         player.opponent.apply_life_damage(len(player.allies))


CARD_POWER = CardPowerNonCombatAttackAW(NAME, CARD_TEXT, remove_from_game=True)
