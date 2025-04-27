import sys

from card_power_on_attack_resolved import CardPowerOnAttackResolved
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Black Takedown Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '127'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Black'
RESTRICTED = False
CARD_TEXT = ('Once per Combat, you may draw a card after performing a successful attack.')


class CardPowerOnAttackResolvedBTD(CardPowerOnAttackResolved):
    def on_condition(self, phase, damage, is_physical):
        return (self.player is phase.player  # attacking
                and not damage.was_stopped())  # successful

    def on_effect(self, phase, damage, is_physical):
        self.player.draw()


CARD_POWER = CardPowerOnAttackResolvedBTD(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False, choice=True)
