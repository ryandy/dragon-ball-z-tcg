import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


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


class CardPowerEnergyDefenseSREM(CardPowerEnergyDefense):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        player.must_pass_attack_until_next_turn()


CARD_POWER = CardPowerEnergyDefenseSREM(NAME, CARD_TEXT)
