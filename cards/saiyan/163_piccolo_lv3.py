import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Piccolo Lv3'
LEVEL = 3
SAGA = 'Saiyan'
CARD_NUMBER = '163'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Piccolo'
IS_HERO = True
POWER_UP_RATING = 3
POWER_STAGES = range(3200, 7700+1, 500)
CARD_TEXT = ('Multi-Form allows two physical attacks, one after another, or a defense against a'
             ' physical attack preventing 4 stages of successful damage.')


class CardPowerMultiForm(CardPowerPhysicalAttack):
    def on_attack(self, player, phase):
        super().on_attack(player, phase)
        super().on_attack(player, phase)


CARD_POWER = [
    CardPowerMultiForm(NAME, CARD_TEXT, exhaust=False, discard=False),
    CardPowerPhysicalDefense(NAME, CARD_TEXT, exhaust=False, discard=False,
                             damage_modifier=DamageModifier(power_prevent=4))
]
