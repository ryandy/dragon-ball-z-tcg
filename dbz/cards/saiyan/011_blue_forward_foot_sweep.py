import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Blue Forward Foot Sweep'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '11'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Blue'
CARD_TEXT = ('Physical Attack doing +4 stages of damage. If successful, this attack stops any'
             ' energy attack from an opponent in their next phase. Lower foe\'s anger level 1.')


class CardPowerPhysicalAttackBFFS(CardPowerPhysicalAttack):
    def on_success(self, player, phase):
        card_power = CardPowerEnergyDefense(
            self.name, self.description, discard=False, is_floating=True)
        card_power.exhaust_after_next_combat_attack_phase()
        player.register_card_power(card_power)


CARD_POWER = CardPowerPhysicalAttackBFFS(
    NAME, CARD_TEXT, damage_modifier=DamageModifier(power_add=4), opp_anger=-1)
