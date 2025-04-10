import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Straining Rolling Escape Move'
SUBTYPE = 'Energy Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '42'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Stops an energy attack, but the user cannot make any attacks for the rest'
             ' of this combat.')


class CardPowerSREM(CardPowerEnergyDefense):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        player.must_pass_attack_until_next_turn()


CARD_POWER = CardPowerSREM(NAME, CARD_TEXT)
