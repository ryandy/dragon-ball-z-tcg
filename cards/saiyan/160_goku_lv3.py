import sys

from cost import Cost
from damage import Damage
from timing import Timing


TYPE = 'Personality'
NAME = 'Goku'
LEVEL = 3
SAGA = 'Saiyan'
CARD_NUMBER = 160
RARITY = 4
CHARACTER = 'Goku'
IS_HERO = True
POWER_UP_RATING = 3
POWER_STAGES = range(8000, 12500+1, 500)
CARD_TEXT = ('Prevent 2 life card draws from being discarded from a successful energy attack.')


_cost = Cost.none()
_damage = Damage.life_damage_reduction(2)  # TODO: Damage modification class?
def _execute(card, player, phase):
    # 4-14. Defender participates, calculate damage, do damage, handle dragon balls
    player.pay_cost(_cost)  # TODO: is there ever cost associated with defense?
    #success = phase.energy_attack(_damage, src=card)  # TODO energy_defense/damage_reduction
    # 16. Register floating effect(s)
    #   None
    # 17. Exhaust/Discard
    player.exhaust_power(card)


CARD_POWER = {
    Timing.ENERGY_DAMAGE_REDUCTION: (_cost, _damage, _execute),
}
