import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


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


class CardPowerMothersDefense(CardPowerPhysicalDefense):
    # Power is always active even when not in control of combat
    def is_deactivated(self):
        return False


CARD_POWER = CardPowerMothersDefense(
    NAME, CARD_TEXT, exhaust=False, discard=False,
    cost=Cost(character_in_control_req=[Character.GOHAN, Character.GOKU]))
