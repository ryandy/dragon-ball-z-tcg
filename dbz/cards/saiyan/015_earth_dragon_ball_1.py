import sys

from dbz.card_power_dragon_ball import CardPowerDragonBall
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Dragon Ball'
NAME = 'Earth Dragon Ball 1'
DB_SET = 'Earth'
DB_NUMBER = 1
SAGA = 'Saiyan'
CARD_NUMBER = '15'
RARITY = 1
DECK_LIMIT = 1
CHARACTER = None
STYLE = None
CARD_TEXT = ('Instantly power up to full and draw a card.')


class CardPowerDragonBallEDB1(CardPowerDragonBall):
    def on_play(self, player, phase):
        personality = player.choose_power_stage_target(10)
        personality.adjust_power_stage(10)
        player.draw()


CARD_POWER = CardPowerDragonBallEDB1(NAME, CARD_TEXT)
