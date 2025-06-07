import sys

from dbz.card_power_on_end_of_turn import CardPowerOnEndOfTurn
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Roshi\'s Calming'
SAGA = 'Saiyan'
CARD_NUMBER = '239'
RARITY = 5
DECK_LIMIT = 1
CHARACTER = 'Master Roshi'
STYLE = None
CARD_TEXT = ('Use at the end of any turn. If your opponent’s Main Personality is at Level 2,'
             ' lower their Main Personality one personality level.')


class CardPowerOnEndOfTurnRC(CardPowerOnEndOfTurn):
    def on_condition(self):
        return self.player.opponent.main_personality.level == 2

    def on_effect(self):
        self.player.opponent.reduce_level()


CARD_POWER = CardPowerOnEndOfTurnRC(NAME, CARD_TEXT, choice=True)
