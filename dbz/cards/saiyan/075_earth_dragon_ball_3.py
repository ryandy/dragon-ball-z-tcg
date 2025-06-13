import sys

from dbz.card_power_dragon_ball import CardPowerDragonBall
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Dragon Ball'
NAME = 'Earth Dragon Ball 3'
DB_SET = 'Earth'
DB_NUMBER = 3
SAGA = 'Saiyan'
CARD_NUMBER = '75'
RARITY = 3
DECK_LIMIT = 1
CHARACTER = None
STYLE = None
CARD_TEXT = ('Draw three cards if you wish, and place the top discarded card at the bottom of your'
             ' life deck.')


class CardPowerDragonBallEDB3(CardPowerDragonBall):
    def on_play(self, player, phase):
        idx = player.choose(['Draw 3 cards.'], [''])
        if idx is not None:
            for _ in range(3):
                player.draw()

        player.rejuvenate()


CARD_POWER = CardPowerDragonBallEDB3(NAME, CARD_TEXT)
