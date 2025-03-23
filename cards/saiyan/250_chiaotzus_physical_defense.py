import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Chiaotzu\'s Physical Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '250'
RARITY = 6
DECK_LIMIT = None
CHARACTER = 'Chiaotzu'
STYLE = None
CARD_TEXT = ('Stops all heroes from losing 1 life card of damage from every attack for the'
             ' remainder of Combat. Remove from the game after use.')


# What if an attack does power stages of damage that convert into life cards?
# So does this card power "prevent" damage or "reduce" it?
# Damage is reduced before it is actually applied (according to the battle sequence)
'''
From 11/24/04 CRD:

Pg. 11:
When an effect “reduces” the damage from an attack, it is modifying the damage and is not
considered “preventing” damage. Attacks that may not be “prevented” may still be affected by cards
that “reduce” damage.

Pg. 15:
Prevent damage from the attack is not counted as modifying damage from the attack.

Pg. 15:
When a personality is at 0 and is dealt power stages of damage, those power stages of damage are
converted into life cards of damage, and is considered both types of damage.

EXAMPLE: Player A’s Main Personality is at 0. Player B performs a physical attack doing 5 power
stages of damage. Player A defends with a card that prevents 3 life cards of damage. Player A
begins to take the 5 power stages of damage, but since his Main Personality is at 0 the 5 power
stages of damage is converted into 5 life cards of damage. Since the damage is both power stages
AND life cards of damage, Player A is able to prevent 3 life cards of damage (because of the card
that he defended with). Player A ends up only taking 2 life cards of damage.

Pg. 44:
Reduce: To “Reduce” damage is modifying damage, and happens during the modification step according
the Battle Sequence (step 9). Reducing damage does not count as a defensive power, since it
modifies an attack, and doesn’t stop the attack or damage from the attack.
'''
# So this seems like reduce = modify, and stop = prevent.
# Damage prevention would then occur right at the time of damage application: power first,
# then life cards.


class CardPowerCPD(CardPowerNonCombatAttack):
    def on_success(self, player, phase):
        class CardPowerCPD_DamageModification(CardPowerOnDamageModification):
            def _on_damage_modification(_self, _attacker, _phase):
                if _attacker.opponent.personality.is_hero:
                    return DamageModifier(life_prevent=1)
            def on_physical_damage_modification(_self, _attacker, _phase):
                return _self._on_damage_modification(_attacker, _phase)
            def on_energy_damage_modification(_self, _attacker, _phase):
                return _self._on_damage_modification(_attacker, _phase)
        card_power = CardPowerCPD_DamageModification(self.name, self.description)
        card_power.exhaust_after_this_turn()
        card_power.set_floating()
        player.register_card_power(card_power)


CARD_POWER = CardPowerCPD(NAME, CARD_TEXT, remove_from_game=True)
