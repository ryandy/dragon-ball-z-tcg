import sys

from card_power_defense import CardPowerEnergyDefense, CardPowerAnyDefense
from card_power_on_discard import CardPowerOnDiscard
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier
from state import State


TYPE = 'Combat'
NAME = 'Saiyan Truce Card'
SUBTYPE = 'Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '203'
RARITY = 5
DECK_LIMIT = 1
CHARACTER = None
STYLE = None
CARD_TEXT = ('End Combat. Until the Rejuvenation Step of your next turn, you may keep any cards in'
             ' your hand during any Rejuvenation Steps. Remove from the game after use.')


class CardPowerOnDiscardSTC(CardPowerOnDiscard):
    def on_effect(self, phase):
        phase.skip_discard[self.player] = True


class CardPowerAnyDefenseSTC(CardPowerAnyDefense):
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


CARD_POWER = CardPowerAnyDefenseSTC(
    NAME, CARD_TEXT, force_end_combat=True, remove_from_game=True)
