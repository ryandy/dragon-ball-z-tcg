import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerAnyDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Ally\'s Sacrifice'
SUBTYPE = 'Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '156'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Stops all of your opponent\'s physical and energy attacks for the remainder of'
             ' Combat. Remove one of your Allies in play from the game to use this card.')


class CardPowerAS(CardPowerAnyDefense):
    def on_resolved(self, player, phase):
        self.resolved_count += 1
        if self.resolved_count == 1:
            self.cost = Cost.none()
            self.exhaust_after_this_turn()
            if self.card:
                player.remove_from_game(self.card, exhaust_card=False)
            self.set_floating()


CARD_POWER = CardPowerAS(NAME, CARD_TEXT, cost=Cost(own_ally=1), remove_from_game=True)
