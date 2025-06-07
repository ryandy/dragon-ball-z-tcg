import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier
from dbz.dragon_ball_card import DragonBallCard
from dbz.util import dprint


TYPE = 'Non-Combat'
NAME = 'Vegeta\'s Trick'
SAGA = 'Saiyan'
CARD_NUMBER = '240'
RARITY = 5
DECK_LIMIT = 1
CHARACTER = 'Vegeta'
STYLE = None
CARD_TEXT = ('Find the foe\'s first Dragon Ball in their Life Deck and place it at the bottom'
             ' of their deck.')


class CardPowerNonCombatAttackVT(CardPowerNonCombatAttack):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        player.debug()

        db_card = None
        for card in reversed(player.opponent.life_deck.cards):
            dprint(f'{player.opponent.name}\'s next card revealed: {card}')
            if isinstance(card, DragonBallCard):
                db_card = card
                break

        if db_card:
            player.opponent.life_deck.remove(db_card)
        else:
            dprint(f'No Dragon Ball card found')

        player.opponent.shuffle_deck()

        if db_card:
            player.opponent.life_deck.add_bottom(db_card)
            dprint(f'{db_card} placed at bottom of {player.opponent.name}\'s deck')


CARD_POWER = CardPowerNonCombatAttackVT(NAME, CARD_TEXT)
