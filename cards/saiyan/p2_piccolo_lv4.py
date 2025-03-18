import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Piccolo Lv4'
LEVEL = 4
SAGA = 'Saiyan'
CARD_NUMBER = 'P2'
RARITY = 2
CHARACTER = 'Piccolo'
IS_HERO = True
POWER_UP_RATING = 4
POWER_STAGES = range(8000, 12500+1, 500)
CARD_TEXT = ('Use Special Beam Cannon or Multi-Form in a combat round.')


class CardPowerMultiForm(CardPowerPhysicalAttack):
    def on_attack(self, player, phase):
        super().on_attack(player, phase)
        super().on_attack(player, phase)


_beam_text = ('Special Energy Beam Cannon. This energy blast only takes 1 power stage to use and'
              ' does 2 life card draws of damage.')
_form_text = ('Multi-Form allows two physical attacks, one after another.')

# TODO: Or single CardPower that then splits and allows user to choose?
CARD_POWER = [
    CardPowerEnergyAttack(
        NAME + ' - Special Beam Cannon', _beam_text,
        exhaust=False, discard=False,
        cost=Cost.energy_attack(power=1),
        damage=Damage.energy_attack(life=2)),
    CardPowerMultiForm(
        NAME + ' - Multi-Form', _form_text,
        exhaust=False, discard=False)
]
