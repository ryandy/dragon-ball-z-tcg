import sys

from dbz.card_power_on_remove_from_play import CardPowerOnRemoveFromPlay
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier
from dbz.style import Style


TYPE = 'Drill'
NAME = 'Goku\'s Mixing Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '231'
RARITY = 5
DECK_LIMIT = None
CHARACTER = 'Goku'
STYLE = None
RESTRICTED = False
CARD_TEXT = ('Allows multiple colors of drills to be used at the same time.')


def _drills_are_legal(player):
    styled_drills = [x for x in player.drills if x.style != Style.FREESTYLE]
    for card in styled_drills:
        if any(x.style != card.style for x in styled_drills):
            return False
    return True


# This card's power is enforced automatically and passively. We just need to re-enforce the rules
# once the drill is removed from play.
class CardPowerOnRemoveFromPlayGMD(CardPowerOnRemoveFromPlay):
    # Called _after_ the card has been removed from play
    def on_remove_from_play(self, player):
        # If another Goku's Mixing Drill remains in play, no need to do anything
        if player.card_in_play('saiyan.231'):  # Goku's Mixing Drill
            return

        while not _drills_are_legal(player):
            # Choose a drill to discard
            cards = [x for x in player.drills if x.style != Style.FREESTYLE]
            assert cards
            idx = player.choose(
                [x.name for x in cards],
                [x.card_text for x in cards],
                allow_pass=False,
                prompt='You have too many drill styles. Select a drill to discard')
            player.discard(cards[idx])


CARD_POWER = CardPowerOnRemoveFromPlayGMD(NAME, CARD_TEXT)
