import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Saibaimen Lv4'
LEVEL = 4
SAGA = 'Saiyan'
CARD_NUMBER = '246'
RARITY = 5
DECK_LIMIT = 1
CHARACTER = 'Saibaimen'
IS_HERO = False
POWER_UP_RATING = 4
POWER_STAGES = range(9000, 18000+1, 1000)
CARD_TEXT = ('If there is more than one Saibaimen in play, this one can make a physical attack'
             ' that inflicts 5 life cards damage.')


class CardPowerSL4(CardPowerPhysicalAttack):
    def is_restricted(self, player):
        cards = (player.allies.cards + player.opponent.allies.cards
                 + [player.main_personality, player.opponent.main_personality])
        if not any((card is not self.card
                    and card.character == Character.SAIBAIMEN) for card in cards):
            return True
        return super().is_restricted(player)


CARD_POWER = CardPowerSL4(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
    damage=Damage(life=5))
