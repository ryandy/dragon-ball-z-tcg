import sys

from dbz.card_power_on_remove_from_play import CardPowerOnRemoveFromPlay
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier
from dbz.style import Style


TYPE = 'Drill'
NAME = 'Orange Focusing Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '234'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Orange'
RESTRICTED = False
CARD_TEXT = ('Your Drills in play except for "Orange Focusing Drill" cannot be discarded or'
             ' removed from the game unless you advance or lose a Personality level.')


# This card's power is enforced automatically and passively. We just need to re-enforce the rules
# once the drill is removed from play because a restricted drill may be in violation now.
class CardPowerOnRemoveFromPlayOFD(CardPowerOnRemoveFromPlay):
    # Called _after_ the card has been removed from play
    def on_remove_from_play(self, player):
        # If another Orange Focusing Drill remains in play, no need to do anything
        if player.card_in_play('saiyan.234'):  # Orange Focusing Drill
            return
        player.discard_invalid_restricted_drills()


CARD_POWER = CardPowerOnRemoveFromPlayOFD(NAME, CARD_TEXT)
