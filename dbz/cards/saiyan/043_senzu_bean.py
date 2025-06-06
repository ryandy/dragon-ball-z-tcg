import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.card_power_dragon_ball import CardPowerDragonBall
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


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


class CardPowerDragonBallSB(CardPowerDragonBall):
    def on_play(self, player, phase):
        player.main_personality.adjust_power_stage(10)
        self.on_resolved()


CARD_POWER = CardPowerDragonBallSB(NAME, CARD_TEXT, remove_from_game=True)
