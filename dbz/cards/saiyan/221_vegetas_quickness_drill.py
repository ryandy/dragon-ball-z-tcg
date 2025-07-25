import sys

from dbz.card_power_on_entering_combat import CardPowerOnEnteringCombat
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Vegeta\'s Quickness Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '221'
RARITY = 5
DECK_LIMIT = 1
CHARACTER = 'Vegeta'
STYLE = None
RESTRICTED = False
CARD_TEXT = ('At the beginning of each combat, draw 1 card from the bottom of the discard pile.')


class CardPowerOnEnteringCombatVQD(CardPowerOnEnteringCombat):
    def on_effect(self, phase):
        if len(self.player.discard_pile) > 0:
            card = self.player.discard_pile.draw_from_bottom()
            self.player.draw(card=card)


CARD_POWER = CardPowerOnEnteringCombatVQD(
    NAME, CARD_TEXT, exhaust=False, discard=False, choice=False)
