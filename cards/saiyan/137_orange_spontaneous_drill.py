import sys

from card_power_on_attack_resolved import CardPowerOnAttackResolved
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Orange Spontaneous Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '137'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Orange'
RESTRICTED = False
CARD_TEXT = ('After taking damage from a physical attack, you may draw the bottom'
             ' card of your discard pile.')


class CardPowerOnAttackResolvedOSD(CardPowerOnAttackResolved):
    def on_condition(self, phase, damage, is_physical):
        return (self.player is not phase.player  # defending
                and is_physical  # physical
                and not damage.was_stopped()  # successful
                and (damage.power > 0 or damage.life > 0)  # did damage
                and len(self.player.discard_pile) > 0)  # card available to draw

    def on_effect(self, phase, damage, is_physical):
        card = self.player.discard_pile.draw_from_bottom()
        self.player.draw(card=card)


CARD_POWER = CardPowerOnAttackResolvedOSD(
    NAME, CARD_TEXT, exhaust=False, discard=False, choice=True)
