import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttackMultiForm
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Piccolo Lv4'
LEVEL = 4
SAGA = 'Saiyan'
CARD_NUMBER = 'P2'
RARITY = 2
DECK_LIMIT = 1
CHARACTER = 'Piccolo'
IS_HERO = True
POWER_UP_RATING = 4
POWER_STAGES = range(8000, 12500+1, 500)
CARD_TEXT = ('Use Special Beam Cannon or Multi-Form in a combat round.')


# Using unique names/descriptions because both are attacks and need to be distinguishable
_beam_text = ('Special Energy Beam Cannon. This energy blast only takes 1 power stage to use and'
              ' does 2 life card draws of damage.')
_form_text = ('Multi-Form allows two physical attacks, one after another.')

CARD_POWER = [
    CardPowerEnergyAttack(
        NAME + ' - Special Energy Beam Cannon', _beam_text,
        exhaust_until_next_turn=True, discard=False,
        cost=Cost.energy_attack(power=1),
        damage=Damage.energy_attack(life=2)),
    CardPowerPhysicalAttackMultiForm(
        NAME + ' - Multi-Form', _form_text,
        exhaust_until_next_turn=True, discard=False)
]
