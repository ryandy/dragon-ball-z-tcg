import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Red Back Kick'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '58'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Red'
CARD_TEXT = ('Physical attack doing +3 stages of damage if successful. Stops all energy attacks'
             ' for the rest of this combat. Foe\'s anger level decreases by 1.')


class CardPowerPhysicalAttackRBK(CardPowerPhysicalAttack):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        defense_text = 'Stops all energy attacks for the rest of this combat.'
        card_power = CardPowerEnergyDefense(
            self.name, defense_text, discard=False, is_floating=True)
        card_power.exhaust_after_this_turn()
        player.register_card_power(card_power)
        player.opponent.register_card_power(card_power.copy())


CARD_POWER = CardPowerPhysicalAttackRBK(
    NAME, CARD_TEXT, opp_anger=-1, damage_modifier=DamageModifier(power_add=3))
