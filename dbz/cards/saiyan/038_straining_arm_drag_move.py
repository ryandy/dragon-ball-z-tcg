import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Straining Arm Drag Move'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '38'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Physical attack doing 1 life card of damage. You must pass in all remaining'
             ' phases of Combat.')


class CardPowerSADM(CardPowerPhysicalAttack):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        player.must_pass_until_next_turn()


CARD_POWER = CardPowerSADM(NAME, CARD_TEXT, damage=Damage(life=1))
