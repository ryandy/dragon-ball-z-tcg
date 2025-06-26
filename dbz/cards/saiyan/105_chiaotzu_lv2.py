import sys

from dbz.card_power_attack import CardPowerPhysicalAttack, CardPowerEnergyAttack
from dbz.card_power_defense import CardPowerPhysicalDefense, CardPowerEnergyDefense
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier
from dbz.exception import GameOver


TYPE = 'Personality'
NAME = 'Chiaotzu Lv2'
LEVEL = 2
SAGA = 'Saiyan'
CARD_NUMBER = '105'
RARITY = 3
DECK_LIMIT = 1
CHARACTER = 'Chiaotzu'
IS_HERO = True
POWER_UP_RATING = 2
POWER_STAGES = range(500, 1400+1, 100)
CARD_TEXT = ('Blast Energy Attack does 6 life cards of damage and removes Chiaotzu from the game.')


class CardPowerEnergyAttackCL2(CardPowerEnergyAttack):
    def on_pay_cost(self, player, phase):
        super().on_pay_cost(player, phase)
        if player.main_personality is self.card:
            raise GameOver(f'{player}\'s Main Personality has been removed from the game',
                           player.opponent)
        if self.card:
            player.remove_from_game(self.card)


CARD_POWER = CardPowerEnergyAttackCL2(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False,
    damage=Damage.energy_attack(life=6))
