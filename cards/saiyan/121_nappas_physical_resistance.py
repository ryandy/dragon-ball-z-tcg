import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Nappa\'s Physical Resistance'
SUBTYPE = 'Physical Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '121'
RARITY = 3
DECK_LIMIT = 1
CHARACTER = 'Nappa'
STYLE = None
CARD_TEXT = ('Stops a physical attack. Stop all physical attacks performed against you for'
             ' the remainder of Combat. Remove from the game after use.')


class CardPowerPhysicalDefenseNPR(CardPowerPhysicalDefense):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        card_power = CardPowerPhysicalDefense(
            self.name, self.description, discard=False, is_floating=True)
        card_power.exhaust_after_this_turn()
        player.register_card_power(card_power)


CARD_POWER = CardPowerPhysicalDefenseNPR(NAME, CARD_TEXT, remove_from_game=True)
