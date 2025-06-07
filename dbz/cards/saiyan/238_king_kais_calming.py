import sys

from dbz.card_power_on_end_of_turn import CardPowerOnEndOfTurn
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'King Kai\'s Calming'
SAGA = 'Saiyan'
CARD_NUMBER = '238'
RARITY = 5
DECK_LIMIT = 1
CHARACTER = 'King Kai'
STYLE = None
CARD_TEXT = ('Use at the end of any turn. If your opponent’s Main Personality is at Level 3,'
             ' lower their Main Personality one personality level.')


class CardPowerOnEndOfTurnKKC(CardPowerOnEndOfTurn):
    def on_condition(self):
        return self.player.opponent.main_personality.level == 3

    def on_effect(self):
        self.player.opponent.reduce_level()


CARD_POWER = CardPowerOnEndOfTurnKKC(NAME, CARD_TEXT, choice=True)
