import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.card_power_on_attack_resolved import CardPowerOnAttackResolved
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


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


class CardPowerOnAttackResolvedGT(CardPowerOnAttackResolved):
    def on_condition(self, phase, damage, is_physical):
        return (self.player is phase.player  # attacking
                and not damage.was_stopped()  # successful
                and is_physical  # physical
                and self.player.can_steal_dragon_ball())  # dragon ball(s) to steal

    def on_effect(self, phase, damage, is_physical):
        self.player.steal_dragon_ball()


CARD_POWER = CardPowerOnAttackResolvedGT(NAME, CARD_TEXT, choice=True, remove_from_game=True)
