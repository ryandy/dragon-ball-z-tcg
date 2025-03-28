import sys

from card_power_on_remove_from_play import CardPowerOnRemoveFromPlay
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier
from style import Style


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
    for card in player.drills:
        if any(x.style != card.style for x in player.drills if x.style != Style.FREESTYLE):
            return False
    return True


# This card's power is enforced automatically and passively. We just need to re-enforce the rules
# once the drill is removed from play.
class CardPowerGMD(CardPowerOnRemoveFromPlay):
    def on_remove_from_play(self, player, phase):
        # If another Goku's Mixing Drill remains in play, no need to do anything
        for card in player.drills:
            if (card is not self.card
                and card.get_id() == self.card.get_id()):
                return

        while not _drills_are_legal(player):
            # Choose a drill to discard
            cards = [x for x in player.drills if x is not self.card and x.style != Style.FREESTYLE]
            assert cards
            idx = player.choose(
                [x.name for x in cards],
                [x.card_text for x in cards],
                allow_pass=False,
                prompt='You have too many drill styles. Select a drill to discard')
            player.discard(cards[idx])


CARD_POWER = CardPowerGMD(NAME, CARD_TEXT)
