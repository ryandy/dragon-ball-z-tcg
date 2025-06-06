import sys

from card_power_on_entering_power_up_phase import CardPowerOnEnteringPowerUpPhase
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Teaching the Unteachable Forces Observation'
SAGA = 'Saiyan'
CARD_NUMBER = '192'
RARITY = 5
DECK_LIMIT = 1
CHARACTER = None
STYLE = None
CARD_TEXT = ('Use this card at the beginning of your opponent\'s Power Up step.'
             ' Your opponent may not declare Combat this turn. Remove from the game after use.')


class CardPowerOnEnteringPowerUpPhaseTTUFO(CardPowerOnEnteringPowerUpPhase):
    def on_condition(self, phase):
        return phase.player is not self.player  # opponent's Power Up step

    def on_effect(self, phase):
        phase.set_force_skip_combat()


CARD_POWER = CardPowerOnEnteringPowerUpPhaseTTUFO(
    NAME, CARD_TEXT, choice=True, remove_from_game=True)
