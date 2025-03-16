import sys

from cost import Cost
from damage import Damage
from timing import Timing


TYPE = 'Personality'
NAME = 'Goku'
LEVEL = 1
SAGA = 'Saiyan'
CARD_NUMBER = 158
RARITY = 4
CHARACTER = 'Goku'
IS_HERO = True
POWER_UP_RATING = 1
POWER_STAGES = range(500, 1400+1, 100)
CARD_TEXT = ('Kamehameha Energy Attack does three life card draw and only costs one power stage to'
             ' perform.')


_cost = Cost.energy_attack(power=1)
_damage = Damage.energy_attack(life_base=3)
def _execute(card, player, phase):
    # 2. Pay cost
    player.pay_cost(_cost)
    # 3. Secondary effects
    #   None
    # 4-14. Defender participates, calculate damage, do damage, handle dragon balls
    success = phase.energy_attack(_damage, src=card)
    # 15. Handle "if successful" effects
    #   None
    # 16. Register floating effect(s)
    #   None
    # 17. Exhaust/Discard
    player.exhaust_power(card)


CARD_POWER = {
    Timing.ATTACK: (_cost, _damage, _execute),
}
