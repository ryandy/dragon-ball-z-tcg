import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.card_power_on_discard import CardPowerOnDiscard
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier
from dbz.state import State


TYPE = 'Combat'
NAME = 'Saiyan Truce Card'
SUBTYPE = 'Combat - Attack'  # Must be used as an attack according to 11/24/04 CRD pg3
SAGA = 'Saiyan'
CARD_NUMBER = '203'
RARITY = 5
DECK_LIMIT = 1
CHARACTER = None
STYLE = 'Saiyan'
CARD_TEXT = ('End Combat. Until the Rejuvenation Step of your next turn, you may keep any cards in'
             ' your hand during any Rejuvenation Steps. Remove from the game after use.')


class CardPowerOnDiscardSTC(CardPowerOnDiscard):
    def on_effect(self, phase):
        phase.skip_discard[self.player] = True


class CardPowerNonCombatAttackSTC(CardPowerNonCombatAttack):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)

        description = ('Until the Rejuvenation Step of your next turn, you may keep any cards in'
                       ' your hand during any Rejuvenation Steps.')
        card_power = CardPowerOnDiscardSTC(
            self.name, description, exhaust=False, discard=False)
        card_power.set_floating()
        if State.TURN_PLAYER is player:
            # Currently player's turn, effect lasts this turn and next turn
            card_power.exhaust_after_turns(1)
        else:
            # Currently opponent's turn, effect lasts this turn
            card_power.exhaust_after_turns(0)
        player.register_card_power(card_power)


CARD_POWER = CardPowerNonCombatAttackSTC(
    NAME, CARD_TEXT, force_end_combat=True, remove_from_game=True)
