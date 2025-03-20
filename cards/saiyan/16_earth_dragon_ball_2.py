import sys

from card_power_dragon_ball import CardPowerDragonBall
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Dragon Ball'
NAME = 'Earth Dragon Ball 2'
DB_SET = 'Earth'
DB_NUMBER = 2
SAGA = 'Saiyan'
CARD_NUMBER = '16'
RARITY = 1
DECK_LIMIT = 1
CHARACTER = None
STYLE = None
CARD_TEXT = ('All foes have their power ratings changed to 2 stages higher than 0.')


class CardPowerEDB2(CardPowerDragonBall):
    def on_play(self, player, phase):
        player.opponent.personality.set_power_stage(2)
        for ally in player.opponent.allies:
            ally.set_power_stage(2)


CARD_POWER = CardPowerEDB2(NAME, CARD_TEXT)
