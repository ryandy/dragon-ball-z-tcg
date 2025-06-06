import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.card_power_on_entering_combat import CardPowerOnEnteringCombat
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Krillin Lv4'
LEVEL = 1
SAGA = 'Saiyan'
CARD_NUMBER = 'P6'
RARITY = 2
DECK_LIMIT = 1
CHARACTER = 'Krillin'
IS_HERO = True
POWER_UP_RATING = 4
POWER_STAGES = range(3200, 7700+1, 500)
CARD_TEXT = ('Draws the bottom two cards from the discard pile to use in this combat.')


class CardPowerOnEnteringCombatKL4(CardPowerOnEnteringCombat):
    def on_effect(self, phase):
        for _ in range(2):
            if len(self.player.discard_pile) > 0:
                card = self.player.discard_pile.draw_from_bottom()
                self.player.draw(card=card)


CARD_POWER = CardPowerOnEnteringCombatKL4(
    NAME, CARD_TEXT, exhaust=False, discard=False)
