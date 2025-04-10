import sys

from card_power_attack import CardPowerNonCombatAttack
from card_power_dragon_ball import CardPowerDragonBall
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Senzu Bean'
SAGA = 'Saiyan'
CARD_NUMBER = '43'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('When you place this card in play, immediately raise your Main Personality to'
             ' its highest power stage. Remove from the game after use.')


class CardPowerSB(CardPowerDragonBall):
    def on_play(self, player, phase):
        player.main_personality.adjust_power_stage(10)
        player.remove_from_game(self.card)


CARD_POWER = CardPowerSB(NAME, CARD_TEXT)
