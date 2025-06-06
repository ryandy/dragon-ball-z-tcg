import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerNonCombatAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.card_power_on_entering_combat import CardPowerOnEnteringCombat
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Nappa HT Lv1'
LEVEL = 1
SAGA = 'Saiyan'
CARD_NUMBER = '185'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Nappa'
IS_HERO = False
POWER_UP_RATING = 1
POWER_STAGES = range(2000, 3800+1, 200)
CARD_TEXT = ('When entering Combat, your Main Personality gains 2 power stages.')


class CardPowerOnEnteringCombatNHL1(CardPowerOnEnteringCombat):
    def on_effect(self, phase):
        self.player.main_personality.adjust_power_stage(2)


CARD_POWER = CardPowerOnEnteringCombatNHL1(
    NAME, CARD_TEXT, exhaust=False, discard=False)
