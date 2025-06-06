import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier
from dbz.util import dprint


TYPE = 'Non-Combat'
NAME = 'Vegeta\'s Dragon Ball Capture'
SAGA = 'Saiyan'
CARD_NUMBER = '241'
RARITY = 5
DECK_LIMIT = 1
CHARACTER = 'Vegeta'
STYLE = None
CARD_TEXT = ('Capture 2 of a foe\'s Dragon Balls and place them at the bottom of their owner\'s'
             ' life deck.')


class CardPowerNonCombatAttackVDBC(CardPowerNonCombatAttack):
    def on_success(self, player, phase):
        for _ in range(2):
            card = player.choose_opponent_dragon_ball(
                prompt='Select a Dragon Ball to capture')
            if card:
                dprint(f'{player} captures {card.name}, returning it to'
                       f' {card.owner.name}\'s life deck')
                player.opponent.exhaust_card(card)
                player.opponent.dragon_balls.remove(card)
                card.owner.life_deck.add_bottom(card)
                card.set_pile(card.owner.life_deck)

CARD_POWER = CardPowerNonCombatAttackVDBC(NAME, CARD_TEXT)
