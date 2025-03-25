import sys

from card_power_dragon_ball import CardPowerDragonBall
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


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


class CardPowerEDB1(CardPowerDragonBall):
    def on_play(self, player, phase):
        # TODO: main/any?
        player.main_personality.set_power_stage_max()
        player.draw()


CARD_POWER = CardPowerEDB1(NAME, CARD_TEXT)
