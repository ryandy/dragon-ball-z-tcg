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
DECK_LIMIT = 1
CHARACTER = 'Piccolo'
IS_HERO = True
POWER_UP_RATING = 4
POWER_STAGES = range(8000, 12500+1, 500)
CARD_TEXT = ('Use Special Beam Cannon or Multi-Form in a combat round.')


class CardPowerMultiForm(CardPowerPhysicalAttack):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resolved_count = 0

    def on_resolved(self, player, phase):
        self.resolved_count += 1
        if self.resolved_count > 2:
            assert False
        elif self.resolved_count == 2:
            player.exhaust_card_until_next_turn(card=self.card)
        else:
            phase.set_skip_next_attack_phase()
            phase.set_next_attack_power(self)


# Using unique names/descriptions because both are attacks and need to be distinguishable
_beam_text = ('Special Energy Beam Cannon. This energy blast only takes 1 power stage to use and'
              ' does 2 life card draws of damage.')
_form_text = ('Multi-Form allows two physical attacks, one after another.')

CARD_POWER = [
    CardPowerEnergyAttack(
        NAME + ' - Special Energy Beam Cannon', _beam_text,
        exhaust=False, discard=False,
        cost=Cost.energy_attack(power=1),
        damage=Damage.energy_attack(life=2)),
    CardPowerMultiForm(
        NAME + ' - Multi-Form', _form_text,
        exhaust=False, discard=False)
]
