import sys

from dbz.card_power_on_damage_applied import CardPowerOnDamageApplied
from dbz.character import Character
from dbz.combat_phase import CombatPhase
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Blue Cradle Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '138'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Blue'
RESTRICTED = False
CARD_TEXT = ('For every life card you lose in combat, your foe\'s Main Personality'
             ' loses 1 power stage.')


class CardPowerOnDamageAppliedBCD(CardPowerOnDamageApplied):
    def on_condition(self, damaged_player, power_damage, life_damage):
        return (self.player is damaged_player
                and life_damage is not None
                and life_damage > 0)

    def on_effect(self, damaged_player, power_damage, life_damage):
        damaged_player.opponent.main_personality.adjust_power_stage(-life_damage)


CARD_POWER = CardPowerOnDamageAppliedBCD(
    NAME, CARD_TEXT, exhaust=False, discard=False, choice=False)
