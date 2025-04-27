import sys

from card_power_on_attack_resolved import CardPowerOnAttackResolved
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Black Free-Style Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '136'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Black'
RESTRICTED = 'Black'
CARD_TEXT = ('After receiving damage from an energy attack, you may draw the bottom card of'
             ' your discard pile. Can\'t be used with any other Black drills in play.')


class CardPowerOnAttackResolvedBFSD(CardPowerOnAttackResolved):
    def on_condition(self, phase, damage, is_physical):
        return (self.player is not phase.player  # defending
                and not is_physical  # energy
                and not damage.was_stopped()  # successful
                and (damage.power > 0 or damage.life > 0)  # did damage
                and len(self.player.discard_pile) > 0)  # card available to draw

    def on_effect(self, phase, damage, is_physical):
        card = self.player.discard_pile.draw_from_bottom()
        self.player.draw(card=card)


CARD_POWER = CardPowerOnAttackResolvedBFSD(
    NAME, CARD_TEXT, exhaust=False, discard=False, choice=True)
