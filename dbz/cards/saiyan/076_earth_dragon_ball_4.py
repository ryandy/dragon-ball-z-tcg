import sys

from card_power_dragon_ball import CardPowerDragonBall
from card_power_on_combat_declared import CardPowerOnCombatDeclared
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Dragon Ball'
NAME = 'Earth Dragon Ball 4'
DB_SET = 'Earth'
DB_NUMBER = 4
SAGA = 'Saiyan'
CARD_NUMBER = '76'
RARITY = 3
DECK_LIMIT = 1
CHARACTER = None
STYLE = None
CARD_TEXT = ('End the very next combat you are forced into before you sustain damage. Your anger'
             ' level increases 2.')


class CardPowerDragonBallEDB4(CardPowerDragonBall):
    def on_play(self, player, phase):
        player.adjust_anger(2)

        class CardPowerOnCombatDeclaredEDB4(CardPowerOnCombatDeclared):
            def on_condition(_self, _phase):
                return _self.player is not _phase.player

            def on_effect(_self, _phase):
                _phase.set_force_skip_phase()

        # self.card has to be passed along so that stealing dragon balls + powers works
        card_text = 'End the very next combat you are forced into before you sustain damage.'
        card_power = CardPowerOnCombatDeclaredEDB4(
            self.name, card_text, choice=False, discard=False, card=self.card)
        player.register_card_power(card_power)


CARD_POWER = CardPowerDragonBallEDB4(NAME, CARD_TEXT)
