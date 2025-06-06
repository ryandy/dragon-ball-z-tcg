import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Blue Hip Spring Throw'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '12'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Blue'
CARD_TEXT = ('Physical Attack doing +2 stages of damage if successful. Stops a foe\'s'
             ' physical attack on their next round. Lower foe\'s anger level 1.')


class CardPowerPhysicalAttackBHST(CardPowerPhysicalAttack):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)

        card_power = CardPowerPhysicalDefense(
            self.name, self.description, discard=False, is_floating=True)
        card_power.exhaust_after_next_combat_attack_phase()
        player.register_card_power(card_power)


CARD_POWER = CardPowerPhysicalAttackBHST(
    NAME, CARD_TEXT, damage_modifier=DamageModifier(power_add=2), opp_anger=-1)
