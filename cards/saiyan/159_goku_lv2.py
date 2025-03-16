import sys

from cost import Cost
from damage import Damage
from timing import Timing


TYPE = 'Personality'
NAME = 'Goku'
LEVEL = 2
SAGA = 'Saiyan'
CARD_NUMBER = 159
RARITY = 4
CHARACTER = 'Goku'
IS_HERO = True
POWER_UP_RATING = 2
POWER_STAGES = range(3200, 7700+1, 500)
CARD_TEXT = ('Kaio-Ken Power Level Booster. Physical attack draining 4 power stages, no matter what'
             ' Goku\'s power is. Do not consult table.')


_cost = Cost.none()
_damage = Damage.physical_attack(power_base=4, use_pat=False)
def _execute(card, player, phase):
    # 2. Pay cost
    player.pay_cost(_cost)
    # 3. Secondary effects
    #   None
    # 4-14. Defender participates, calculate damage, do damage, handle dragon balls
    success = phase.physical_attack(_damage, src=card)
    # 15. Handle "if successful" effects
    #   None
    # 16. Register floating effect(s)
    #   None
    # 17. Exhaust/Discard
    player.exhaust_power(card)


CARD_POWER = {
    Timing.ATTACK: (_cost, _damage, _execute),
}
