import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.card_power_defense import CardPowerAnyDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Baba\'s Energy Blast'
SAGA = 'Saiyan'
CARD_NUMBER = '225'
RARITY = 5
DECK_LIMIT = None
CHARACTER = 'Baba'
STYLE = None
CARD_TEXT = ('Use when needed. Your opponent discards 3 cards from their Life Deck.'
             ' Remove from the game after use.')


class CardPowerNonCombatAttackBEB(CardPowerNonCombatAttack):
    # Unblockable 3 life damage
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        player.opponent.apply_life_damage(3)


class CardPowerAnyDefenseBEB(CardPowerAnyDefense):
    # Unblockable 3 life damage
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        player.opponent.apply_life_damage(3)


CARD_POWER = [
    CardPowerNonCombatAttackBEB(
        NAME, CARD_TEXT, remove_from_game=True),
    CardPowerAnyDefenseBEB(
        NAME, CARD_TEXT, remove_from_game=True,
        damage_modifier=DamageModifier.none())
]
