import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.card_power_on_anger_adjusted import CardPowerOnAngerAdjusted
from dbz.card_power_on_damage_applied import CardPowerOnDamageApplied
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier
from dbz.state import State


TYPE = 'Combat'
NAME = 'Terrible Wounds'
SUBTYPE = 'Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '208'
RARITY = 5
DECK_LIMIT = 1
CHARACTER = None
STYLE = None
CARD_TEXT = ('Attach this to your opponent\'s Main Personality card. Reset the personality\'s anger'
             ' to (0). It cannot go up until after they force another player to discard'
             ' a life card. Remove from the game after use.')


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
        # This is likely redundant, as this power's resolution will cause the source card
        # to be discarded and all associated card powers to be exhausted.
        self.player.exhaust_card_power(self.anger_card_power)


class CardPowerNonCombatAttackTW(CardPowerNonCombatAttack):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        player.exhaust_card_power(self)  # Exhaust this NonCombatAttack power, but not below powers

        # If somehow called without access to card, attachment does not happen and card does nothing
        if not self.card:
            return

        # Attach to opp personality rather than discard
        self.card.attach_to(player.opponent.main_personality)

        anger_description = ('The foe\'s anger cannot go up until after they force another player'
                             ' to discard a life card.')
        anger_card_power = CardPowerOnAngerAdjustedTW(
            self.name, anger_description, exhaust=False, discard=False, card=self.card)
        registered_anger_card_power = player.register_card_power(anger_card_power)

        damage_description = ('When the foe forces another player to discard a life card,'
                              ' this card\'s effect is no longer active.')
        damage_card_power = CardPowerOnDamageAppliedTW(
            f'{self.name} (expiry)', damage_description,
            card=self.card, silent=True, exhaust=True, discard=True,
            anger_card_power=registered_anger_card_power)
        player.register_card_power(damage_card_power)


CARD_POWER = CardPowerNonCombatAttackTW(
    NAME, CARD_TEXT, opp_anger=-5, exhaust=False, discard=False)
