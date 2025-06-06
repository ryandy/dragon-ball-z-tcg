import sys

from card_power_on_entering_combat import CardPowerOnEnteringCombat
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Meditation Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '149'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = None
RESTRICTED = False
CARD_TEXT = ('When entering Combat, you may shuffle your Life Deck or discard pile.')


class CardPowerOnEnteringCombatMD(CardPowerOnEnteringCombat):
    def on_effect(self, phase):
        idx = self.player.choose(
            ['Shuffle Life Deck', 'Shuffle discard pile'], [''], allow_pass=True)
        if idx == 0:
            self.player.shuffle_deck()
        elif idx == 1:
            self.player.shuffle_discard_pile()


CARD_POWER = CardPowerOnEnteringCombatMD(
    NAME, CARD_TEXT, exhaust=False, discard=False, choice=False)
