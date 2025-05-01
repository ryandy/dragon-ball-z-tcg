import sys

from card_power_on_power_adjusted import CardPowerOnPowerAdjusted
from character import Character
from combat_phase import CombatPhase
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Red Wrist Control Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '139'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Red'
RESTRICTED = False
CARD_TEXT = ('For every 3 power stages you lose, your foe\'s Main Personality loses 1 power stage.')


class CardPowerOnPowerAdjustedRWCD(CardPowerOnPowerAdjusted):
    def on_condition(self, adjusted_player, personality, amount):
        return (self.player is adjusted_player
                and amount <= -3
                and self.player.opponent.main_personality.power_stage > 0)

    def on_effect(self, adjusted_player, personality, amount):
        self.player.opponent.main_personality.reduce_power_stage(abs(amount) // 3)


CARD_POWER = CardPowerOnPowerAdjustedRWCD(
    NAME, CARD_TEXT, exhaust=False, discard=False, choice=False)
