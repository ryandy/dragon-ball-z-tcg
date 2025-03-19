import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Blue Forward Foot Sweep'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '11'
RARITY = 1
CHARACTER = None
STYLE = 'Blue'
CARD_TEXT = ('Physical Attack doing +4 stages of damage. If successful, this attack stops any'
             ' energy attack from an opponent in their next phase. Lower foe\'s anger level 1.')


class CardPowerBFFS(CardPowerPhysicalAttack):
    def on_success(self, player, phase):
        card_power = CardPowerEnergyDefense(
            self.name, self.description, discard=False, is_floating=True)
        card_power.exhaust_after_next_combat_phase()
        #print(f'success! registering energy defense power for {player.name()}')
        player.register_card_power(card_power)


CARD_POWER = CardPowerBFFS(
    NAME, CARD_TEXT, damage_modifier=DamageModifier(power_add=4), opp_anger=-1)
