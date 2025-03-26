import sys

from card_power_attack import CardPowerNonCombatAttack
from card_power_dragon_ball import CardPowerDragonBall
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Dragon Ball'
NAME = 'Earth Dragon Ball 6'
DB_SET = 'Earth'
DB_NUMBER = 6
SAGA = 'Saiyan'
CARD_NUMBER = '186'
RARITY = 5
DECK_LIMIT = 1
CHARACTER = None
STYLE = None
CARD_TEXT = ('This card ends a combat and the user is powered up to full. Shift all opponents\''
             ' anger levels down 2.')


class CardPowerEDB6(CardPowerDragonBall):
    def on_play(self, player, phase):
        player.opponent.adjust_anger(-2)
        card_text = 'This card ends a combat and the user is powered up to full.'
        card_power = CardPowerNonCombatAttack(
            self.name, card_text, main_power=10, force_end_combat=True, card=self.card)
        player.register_card_power(card_power)


CARD_POWER = CardPowerEDB6(NAME, CARD_TEXT)
