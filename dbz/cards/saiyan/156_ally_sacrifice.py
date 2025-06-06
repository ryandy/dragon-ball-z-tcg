import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerAnyDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


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


class CardPowerAnyDefenseAS(CardPowerAnyDefense):
    def on_resolved(self):
        self.resolved_count += 1
        if self.resolved_count == 1:
            self.cost = Cost.none()
            self.exhaust_after_this_turn()
            if self.card:
                self.player.discard(self.card, exhaust_card=False)
            self.set_floating()


CARD_POWER = CardPowerAnyDefenseAS(NAME, CARD_TEXT, cost=Cost(own_ally=1))
