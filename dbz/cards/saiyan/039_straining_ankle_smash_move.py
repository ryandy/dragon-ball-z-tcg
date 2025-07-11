import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerAnyDefense
from dbz.character import Character
from dbz.combat_defense_phase import CombatDefensePhase
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier
from dbz.state import State


TYPE = 'Combat'
NAME = 'Straining Ankle Smash Move'
SUBTYPE = 'Energy Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '39'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Use immediately after your opponent attacks you (physical or energy) and pays'
             ' any costs for that attack. Lower your opponent\'s Main Personality 4 power'
             ' stages immediately when played.')


class CardPowerAnyDefenseSASM(CardPowerAnyDefense):
    def is_restricted(self, player):
        # Can be called at various times, so need to check that the phase is what we expect
        if (isinstance(State.PHASE, CombatDefensePhase)
            and not State.PHASE.attack_phase.attack_power.cost.is_none()):
            return True
        return super().is_restricted(player)


CARD_POWER = CardPowerAnyDefenseSASM(
    NAME, CARD_TEXT, damage_modifier=DamageModifier.none(), opp_power=-4)
