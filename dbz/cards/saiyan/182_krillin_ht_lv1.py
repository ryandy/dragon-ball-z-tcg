import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from card_power_on_entering_combat import CardPowerOnEnteringCombat
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Krillin HT Lv1'
LEVEL = 1
SAGA = 'Saiyan'
CARD_NUMBER = '182'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Krillin'
IS_HERO = True
POWER_UP_RATING = 1
POWER_STAGES = range(100, 1000+1, 100)
CARD_TEXT = ('Draw a card when entering Combat.')


class CardPowerOnEnteringCombatKHL1(CardPowerOnEnteringCombat):
    def on_effect(self, phase):
        self.player.draw()


CARD_POWER = CardPowerOnEnteringCombatKHL1(
    NAME, CARD_TEXT, exhaust=False, discard=False)
