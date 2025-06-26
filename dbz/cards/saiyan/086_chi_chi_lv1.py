import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_defense import CardPowerPhysicalDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Chi-Chi Lv1'
LEVEL = 1
SAGA = 'Saiyan'
CARD_NUMBER = '86'
RARITY = 3
DECK_LIMIT = 1
CHARACTER = 'Chi-Chi'
IS_HERO = True
POWER_UP_RATING = 1
POWER_STAGES = range(100, 1000+1, 100)
CARD_TEXT = ('Mother\'s Defense. Once per combat, this can block a single physical attack directed'
             ' at Gohan or Goku so they are not hurt.')


class CardPowerPhysicalDefenseCCL1(CardPowerPhysicalDefense):
    # Power is always active even when not in control of combat
    def is_deactivated(self):
        return False

    def is_restricted(self, player):
        if (player.control_personality.character != Character.GOHAN
            and player.control_personality.character != Character.GOKU):
            return True
        return super().is_restricted(player)


CARD_POWER = CardPowerPhysicalDefenseCCL1(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False)
