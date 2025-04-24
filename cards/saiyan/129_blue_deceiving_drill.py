import sys

from card_power_on_entering_combat import CardPowerOnEnteringCombat
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Blue Deceiving Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '129'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Blue'
RESTRICTED = False
CARD_TEXT = ('When entering Combat as the defender, you may gain up to 3 power stages.')


class CardPowerOnEnteringCombatBDD(CardPowerOnEnteringCombat):
    def on_condition(self, phase):
        return self.player is not phase.player  # entering combat as the defender

    def on_effect(self, phase):
        personality = self.player.choose_power_stage_target(3)
        personality.adjust_power_stage(3)


CARD_POWER = CardPowerOnEnteringCombatBDD(
    NAME, CARD_TEXT, exhaust=False, discard=False, choice=True)
