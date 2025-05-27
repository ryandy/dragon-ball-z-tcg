import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier
from state import State
from util import dprint


TYPE = 'Combat'
NAME = 'Tien Mind Reading Trick'
SUBTYPE = 'Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '211'
RARITY = 5
DECK_LIMIT = None
CHARACTER = 'Tien'
STYLE = None
CARD_TEXT = ('Attach this to your opponent\'s Main Personality. If Tien is in play, all villain'
             ' opponents must play with their hands face up on the table.')


# This card's power is enforced automatically and passively.
class CardPowerNonCombatAttackTMRT(CardPowerNonCombatAttack):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)

        # If somehow called without access to card, attachment does not happen and card does nothing
        if not self.card:
            return

        # Attach to opp personality rather than discard
        self.card.attach_to(player.opponent.main_personality)

        # One-time review of opp's hand if applicable
        if (player.interactive
            and player.character_in_play(Character.TIEN, either_side=True)
            and not player.opponent.main_personality.is_hero):
            for card in player.opponent.hand:
                dprint(f'{player.opponent} has {card} in hand')


CARD_POWER = CardPowerNonCombatAttackTMRT(NAME, CARD_TEXT, exhaust=True, discard=False)
