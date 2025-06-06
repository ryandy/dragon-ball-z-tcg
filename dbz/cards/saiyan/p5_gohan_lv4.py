import sys

from card_power_on_entering_combat import CardPowerOnEnteringCombat
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Gohan Lv4'
LEVEL = 4
SAGA = 'Saiyan'
CARD_NUMBER = 'P5'
RARITY = 2
DECK_LIMIT = 1
CHARACTER = 'Gohan'
IS_HERO = True
POWER_UP_RATING = 4
POWER_STAGES = range(3200, 7700+1, 500)
CARD_TEXT = ('Draws an extra card from the bottom of the discard pile for this combat.')


class CardPowerOnEnteringCombatGL4(CardPowerOnEnteringCombat):
    def on_effect(self, phase):
        if len(self.player.discard_pile) > 0:
            card = self.player.discard_pile.draw_from_bottom()
            self.player.draw(card=card)


CARD_POWER = CardPowerOnEnteringCombatGL4(
    NAME, CARD_TEXT, exhaust=False, discard=False, choice=False)
