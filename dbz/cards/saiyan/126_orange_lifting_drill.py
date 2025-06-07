import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


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
        drills_to_remove = []
        for drill_card in reversed(player.opponent.drills.cards):
            if drill_card.can_be_removed(player.opponent):
                drills_to_remove.append(drill_card)
        for drill_card in drills_to_remove:
            player.opponent.discard(drill_card)


CARD_POWER = CardPowerNonCombatAttackOLD(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False)
