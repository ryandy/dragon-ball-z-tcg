import sys

from card_power_attack import CardPowerPhysicalAttack, CardPowerEnergyAttack
from card_power_defense import CardPowerPhysicalDefense, CardPowerEnergyDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Gohan Lv1'
LEVEL = 1
SAGA = 'Saiyan'
CARD_NUMBER = '164'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Gohan'
IS_HERO = True
POWER_UP_RATING = 1
POWER_STAGES = range(100, 1000+1, 100)
CARD_TEXT = ('If a successful energy attack is performed against Gohan, he may raise his anger'
             ' 1 level once per combat.')


class CardPowerEnergyDefenseGL1(CardPowerEnergyDefense):
    # Only relevant when Gohan is the Main and controlling Personality
    # This power is only activated when Gohan is controlling, so only need to check for Main
    def is_restricted(self, player):
        if player.main_personality.character != Character.GOHAN:
            return True
        return super().is_restricted(player)


CARD_POWER = CardPowerEnergyDefenseGL1(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
    own_anger=1, damage_modifier=DamageModifier.none())
