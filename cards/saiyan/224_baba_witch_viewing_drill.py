import sys

from card_power_dragon_ball import CardPowerDragonBall
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier
#from state import State  # TODO Delete
from util import dprint


TYPE = 'Drill'
NAME = 'Baba Witch Viewing Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '224'
RARITY = 5
DECK_LIMIT = None
CHARACTER = 'Baba'
STYLE = None
RESTRICTED = False
CARD_TEXT = ('Forces every villain opponent to constantly show their hand of cards face up.')


class CardPowerDragonBallBWVD(CardPowerDragonBall):
    def on_play(self, player, phase):
        # One-time review of opp's hand if applicable
        #player.debug()
        if (player.interactive
            and not player.opponent.main_personality.is_hero):
            for card in player.opponent.hand:
                dprint(f'{player.opponent} has {card} in hand')
                dprint(f'  - {card.card_text}')
        #else:
        #    player.interactive = False
        #    State.INTERACTIVE = False
        self.on_resolved()


# This card's power is enforced automatically and passively.
CARD_POWER = CardPowerDragonBallBWVD(NAME, CARD_TEXT, exhaust=True, discard=False)
