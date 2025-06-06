import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Saiyan Sweeping Defense'
SUBTYPE = 'Physical Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '96'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Saiyan'
CARD_TEXT = ('Saiyan Heritage only. Stops a physical attack and stops a physical attack during'
             ' your opponent\'s next Attacker Attacks phase.')


class CardPowerPhysicalDefenseSSD(CardPowerPhysicalDefense):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        card_power = CardPowerPhysicalDefense(
            self.name, self.description, discard=False, is_floating=True)
        card_power.exhaust_after_next_combat_attack_phase()
        player.register_card_power(card_power)


CARD_POWER = CardPowerPhysicalDefenseSSD(NAME, CARD_TEXT, saiyan_only=True)
