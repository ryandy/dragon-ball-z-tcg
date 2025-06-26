import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Black Fore Fist Punch'
SUBTYPE = 'Energy Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '65'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Black'
CARD_TEXT = ('Energy attack doing 6 life cards of damage. If successful, your opponent loses'
             ' 3 power stages.')


class CardPowerEnergyAttackBFFP(CardPowerEnergyAttack):
    def on_success(self, player, phase):
        # TODO: Do they get to choose which personality?
        # Note: If they chose, would they be able to choose a personality with less than 3 power?
        player.opponent.main_personality.adjust_power_stage(-3)


CARD_POWER = CardPowerEnergyAttackBFFP(NAME, CARD_TEXT, damage=Damage(life=6))
