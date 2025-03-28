import sys

from card_power_attack import CardPowerNonCombatAttack
from card_power_on_attack_resolved import CardPowerOnAttackResolved
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier
from state import State


TYPE = 'Non-Combat'
NAME = 'Goku\'s Touch'
SAGA = 'Saiyan'
CARD_NUMBER = '48'
RARITY = 1
DECK_LIMIT = None
CHARACTER = 'Goku'
STYLE = None
CARD_TEXT = ('Use after you perform a successful physical attack to capture an opponent\'s'
             ' Dragon Ball. Remove from the game after use.')


class CardPowerGT(CardPowerOnAttackResolved):
    def on_condition(self, phase, damage, is_physical):
        return (self.player is phase.player  # attacking
                and not damage.was_stopped()  # successful
                and is_physical  # physical
                and len(self.player.opponent.dragon_balls) > 0)  # dragon ball(s) to steal

    def on_effect(self, phase, damage, is_physical):
        self.player.steal_dragon_ball()


CARD_POWER = CardPowerGT(NAME, CARD_TEXT, choice=True, remove_from_game=True)
