import sys

from card_power_attack import CardPowerNonCombatAttack
from card_power_on_anger_adjusted import CardPowerOnAngerAdjusted
from card_power_on_damage_applied import CardPowerOnDamageApplied
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier
from state import State


TYPE = 'Combat'
NAME = 'Terrible Wounds'
SUBTYPE = 'Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '208'
RARITY = 5
DECK_LIMIT = 1
CHARACTER = None
STYLE = None
CARD_TEXT = ('Place this on a foe\'s Main Personality card. Reset the personality\'s anger to (0).'
             ' It cannot go up until after they force another player to discard a life card.'
             ' Remove from the game after use.')


class CardPowerOnAngerAdjustedTW(CardPowerOnAngerAdjusted):
    def on_condition(self, adjusted_player, amount):
        return (adjusted_player is not self.player
                and amount > 0)

    # Whenever the opponent adjusts their anger by 1+, set the adjustment to 0
    def on_effect(self, adjusted_player, amount):
        return 0


class CardPowerOnDamageAppliedTW(CardPowerOnDamageApplied):
    def __init__(self, *args, **kwargs):
        anger_card_power = kwargs.pop('anger_card_power', None)
        super().__init__(*args, **kwargs)
        self.anger_card_power = anger_card_power

    def on_condition(self, damaged_player, power_damage, life_damage):        
        return (damaged_player is self.player
                and life_damage is not None
                and life_damage > 0)

    def on_effect(self, damaged_player, power_damage, life_damage):
        self.player.exhaust_card_power(self.anger_card_power)


class CardPowerNonCombatAttackTW(CardPowerNonCombatAttack):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)

        anger_description = ('The foe\'s anger cannot go up until after they force another player'
                             ' to discard a life card.')
        anger_card_power = CardPowerOnAngerAdjustedTW(
            self.name, anger_description, exhaust=False, discard=False)
        anger_card_power.set_floating()
        registered_anger_card_power = player.register_card_power(anger_card_power)

        damage_description = ('When the foe forces another player to discard a life card,'
                              ' this card\'s effect is no longer active.')
        damage_card_power = CardPowerOnDamageAppliedTW(
            f'{self.name} (expiry)', damage_description, exhaust=True, discard=False,
            anger_card_power=registered_anger_card_power)
        damage_card_power.set_floating()
        player.register_card_power(damage_card_power)


CARD_POWER = CardPowerNonCombatAttackTW(
    NAME, CARD_TEXT, opp_anger=-5, remove_from_game=True)
