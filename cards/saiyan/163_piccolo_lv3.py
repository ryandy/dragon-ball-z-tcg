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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resolved_count = 0

    def on_resolved(self, player, phase):
        self.resolved_count += 1
        if self.resolved_count > 2:
            assert False
        elif self.resolved_count == 2:
            player.exhaust_card_until_next_turn(card=self.card)
        else:
            phase.set_skip_next_attack_phase()
            phase.set_next_attack_power(self)


CARD_POWER = [
    CardPowerMultiForm(NAME, CARD_TEXT, exhaust=False, discard=False),
    CardPowerPhysicalDefense(NAME, CARD_TEXT, exhaust=False, discard=False,
                             damage_modifier=DamageModifier(power_prevent=4))
]
