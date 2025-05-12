import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from card_power_on_attack_resolved import CardPowerOnAttackResolved
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Vegeta Lv3'
LEVEL = 3
SAGA = 'Saiyan'
CARD_NUMBER = '175'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Vegeta'
IS_HERO = False
POWER_UP_RATING = 4
POWER_STAGES = range(9000, 18000+1, 1000)
CARD_TEXT = ('Captures one Dragon Ball once per game after a successful energy attack. This ends'
             ' the combat step.')


class CardPowerOnAttackResolvedVL3(CardPowerOnAttackResolved):
    def on_condition(self, phase, damage, is_physical):
        return (not hasattr(self.card, '_once_per_game_used')  # once per game
                and self.player is phase.player  # attacking
                and not damage.was_stopped()  # successful
                and is_physical is False  # energy
                and self.player.can_steal_dragon_ball())  # dragon ball(s) to steal

    def on_effect(self, phase, damage, is_physical):
        setattr(self.card, '_once_per_game_used', True)
        self.player.steal_dragon_ball()
        phase.set_force_end_combat()


CARD_POWER = CardPowerOnAttackResolvedVL3(NAME, CARD_TEXT, discard=False, choice=True)
