import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Saiyan Neck Hold'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '21'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Saiyan'
CARD_TEXT = ('Saiyan Heritage only. Physical attack. If successful, it stops a single named foe'
             ' from making a physical attack on their next phase. Costs 2 power stages to perform.')


class CardPowerPhysicalAttackSNH(CardPowerPhysicalAttack):
    def on_success(self, player, phase):
        card_power = CardPowerPhysicalDefense(
            self.name, self.description, discard=False, is_floating=True)
        card_power.exhaust_after_next_combat_attack_phase()
        player.register_card_power(card_power)


CARD_POWER = CardPowerPhysicalAttackSNH(NAME, CARD_TEXT, saiyan_only=True, cost=Cost(power=2))
