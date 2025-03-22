import sys

from card_power_attack import CardPowerNonCombatAttack
from card_power_dragon_ball import CardPowerDragonBall
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Dragon Ball'
NAME = 'Earth Dragon Ball 7'
DB_SET = 'Earth'
DB_NUMBER = 7
SAGA = 'Saiyan'
CARD_NUMBER = '187'
RARITY = 5
DECK_LIMIT = 1
CHARACTER = None
STYLE = None
CARD_TEXT = ('Play this card during combat to end the battle. Pick 3 cards out of your discard'
             ' pile and place them at the top of your life deck. All opponents\' anger levels'
             ' shift down 2.')


# Two card powers:
#   - dragon ball power that just does the basic stuff if played during non-combat
#   - attack power that also ends combat
#     - card power registered when drawn
#     - card power needs to be exhausted if/when played during non-combat


class CardPowerEDB7_DragonBall(CardPowerDragonBall):
    def on_play(self, player, phase):
        player.opponent.adjust_anger(-2)

        for _ in range(3):
            card = player.choose_discard_pile_card()
            if card:
                player.discard_pile.remove(card)
                player.life_deck.add_top(card)
                card.set_pile(player.life_deck)

        # Need to exhaust the registered attack card power
        assert self.card
        player.exhaust_card(self.card)


class CardPowerEDB7_Attack(CardPowerNonCombatAttack):
    def on_success(self, player, phase):
        for _ in range(3):
            card = player.choose_discard_pile_card()
            if card:
                player.discard_pile.remove(card)
                player.life_deck.add_top(card)
                card.set_pile(player.life_deck)

    def on_resolved(self, player, phase):
        assert self.card
        player.exhaust_card(self.card)

        # Card is played from hand so must be put into DB area
        assert self.card.pile is player.hand
        player.hand.remove(self.card)
        player.dragon_balls.add(self.card)
        self.card.set_pile(player.dragon_balls)


CARD_POWER = [
    CardPowerEDB7_DragonBall(NAME, CARD_TEXT),
    CardPowerEDB7_Attack(NAME, CARD_TEXT, opp_anger=-2, end_combat=True)
]
