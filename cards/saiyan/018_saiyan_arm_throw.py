import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Saiyan Arm Throw'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '18'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Saiyan'
CARD_TEXT = ('Saiyan Heritage only. Physical attack. If successful, it stops a single named foe'
             ' from making a physical attack on their next phase.')


# TODO: I don't think this card power is being handled correctly. I think the opponent cannot
#       make any physical/energy attack at all next phase. They would have to
#       do a different kind of attack or pass.
# Note: There is no errata for this card, but there is for 94:
#       "If successful, your opponent cannot perform a physical attack during his next
#        Attacker Attacks phase.”
# Note: Other similar cards: 18, 19, 21, 94
class CardPowerSAT(CardPowerPhysicalAttack):
    def on_success(self, player, phase):
        card_power = CardPowerPhysicalDefense(
            self.name, self.description, discard=False, is_floating=True)
        card_power.exhaust_after_next_combat_attack_phase()
        player.register_card_power(card_power)


CARD_POWER = CardPowerSAT(NAME, CARD_TEXT, saiyan_only=True)
