import sys

from card_power_dragon_ball import CardPowerDragonBall
from card_power_on_combat_declared import CardPowerOnCombatDeclared
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier
from util import dprint


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


class CardPowerEDB4(CardPowerDragonBall):
    def on_play(self, player, phase):
        player.adjust_anger(2)

        class CardPowerEDB4_OnCombatDeclared(CardPowerOnCombatDeclared):
            def on_combat_declared(_self, _player, _phase):
                if _phase.player is not _player:
                    dprint(f'{_player}\'s {_self.name} ends combat')
                    _phase.skipped = True
                    _player.exhaust_card_power(_self)

        card_text = 'End the very next combat you are forced into before you sustain damage.'
        card_power = CardPowerEDB4_OnCombatDeclared(self.name, card_text, card=self.card)
        player.register_card_power(card_power)


CARD_POWER = CardPowerEDB4(NAME, CARD_TEXT)
