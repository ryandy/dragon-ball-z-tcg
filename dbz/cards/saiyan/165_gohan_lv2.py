import sys

from card_power_attack import CardPowerPhysicalAttack, CardPowerEnergyAttack
from card_power_defense import CardPowerPhysicalDefense, CardPowerEnergyDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier
from state import State


TYPE = 'Personality'
NAME = 'Gohan Lv2'
LEVEL = 2
SAGA = 'Saiyan'
CARD_NUMBER = '165'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Gohan'
IS_HERO = True
POWER_UP_RATING = 2
POWER_STAGES = range(500, 1400+1, 100)
CARD_TEXT = ('Once during the game, he can turn into Kong Gohan, inflicting 8 stages of physical'
             ' damage in his first round of combat.')


class CardPowerPhysicalAttackGL2(CardPowerPhysicalAttack):
    def is_restricted(self, player):
        # Can only be used the turn Gohan is played
        if self.card and self.card.play_turn != State.TURN:
            return True

        # Can only be used once per game
        # Card powers can be copied, but cards never are, so store this property on the card
        # This will prevent the power from being reusable, even if Gohan levels back down to 2 later
        if self.card and hasattr(self.card, '_once_per_game_used'):
            return True

        return super().is_restricted(player)

    def on_secondary_effects(self, player, phase):
        # Store this property regardless of attack success
        if self.card:
            setattr(self.card, '_once_per_game_used', True)


CARD_POWER = CardPowerPhysicalAttackGL2(
    NAME, CARD_TEXT, discard=False,
    damage=Damage(power=8))
