import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Saiyan Energy Aura'
SUBTYPE = 'Energy Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '95'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Saiyan'
CARD_TEXT = ('Saiyan Heritage only. Stops an energy attack and stops an energy attack during'
             ' your opponent\'s next Attacker Attacks phase.')


class CardPowerEnergyDefenseSEA(CardPowerEnergyDefense):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        card_power = CardPowerEnergyDefense(
            self.name, self.description, discard=False, is_floating=True)
        card_power.exhaust_after_next_combat_attack_phase()
        player.register_card_power(card_power)


CARD_POWER = CardPowerEnergyDefenseSEA(NAME, CARD_TEXT, saiyan_only=True)
