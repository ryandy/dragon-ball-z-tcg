import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Nappa\'s Energy Aura'
SUBTYPE = 'Energy Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '120'
RARITY = 3
DECK_LIMIT = 1
CHARACTER = 'Nappa'
STYLE = None
CARD_TEXT = ('Stops an energy attack. Stops all energy attacks performed against you for'
             ' the remainder of Combat. Remove from the game after use.')


class CardPowerEnergyDefenseNEA(CardPowerEnergyDefense):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        card_power = CardPowerEnergyDefense(
            self.name, self.description, discard=False, is_floating=True)
        card_power.exhaust_after_this_turn()
        player.register_card_power(card_power)


CARD_POWER = CardPowerEnergyDefenseNEA(NAME, CARD_TEXT, remove_from_game=True)
