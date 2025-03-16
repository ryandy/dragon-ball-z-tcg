import sys

from cost import Cost
from damage import Damage
from timing import Timing


TYPE = 'Combat'
NAME = 'Orange Standing Fist Punch'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = 1
RARITY = 1
CHARACTER = None
STYLE = 'Orange'
CARD_TEXT = ('Physical Attack. Raise card user\'s anger level 1.')


_cost = Cost.none()
_damage = Damage.physical_attack()
def _execute(card, player, phase):
    # 2. Pay cost
    player.pay_cost(_cost)
    # 3. Secondary effects
    player.raise_anger(1)
    # 4-14. Defender participates, calculate damage, do damage, handle dragon balls
    success = phase.physical_attack(_damage, src=card)
    # 15. Handle "if successful" effects
    #   None
    # 16. Register floating effect(s)
    #   None
    # 17. Exhaust/Discard
    player.exhaust_power(card)
    player.discard(card)


CARD_POWER = {
    Timing.ATTACK: (_cost, _damage, _execute),
}
