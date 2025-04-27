import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Orange Lifting Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '126'
RARITY = 3
DECK_LIMIT = 1
CHARACTER = None
STYLE = 'Orange'
RESTRICTED = False
CARD_TEXT = ('Once per Combat, in place of an attack, discard all of your opponents\' Drills.')


class CardPowerNonCombatAttackOLD(CardPowerNonCombatAttack):
    def is_restricted(self, player):
        if len(player.opponent.drills) == 0:
            return True
        return super().is_restricted(player)

    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        # Discard/exhaust all opponent drills
        while len(player.opponent.drills) > 0:
            card = player.opponent.drills.cards[-1]
            player.opponent.discard(card)


CARD_POWER = CardPowerNonCombatAttackOLD(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False)
