import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Tien Lv2'
LEVEL = 2
SAGA = 'Saiyan'
CARD_NUMBER = '83'
RARITY = 3
DECK_LIMIT = 1
CHARACTER = 'Tien'
IS_HERO = True
POWER_UP_RATING = 2
POWER_STAGES = range(500, 1400+1, 100)
CARD_TEXT = ('Solar Flare Energy Attack. If it is not blocked, it stuns the foe, so they must skip'
             ' their next opportunity to attack back.')


class CardPowerSolarFlare(CardPowerEnergyAttack):
    def on_success(self, player, phase):
        phase.set_skip_next_attack_phase()


CARD_POWER = CardPowerSolarFlare(NAME, CARD_TEXT, exhaust=False, discard=False)
