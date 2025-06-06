import sys

from dbz.card_power_attack import CardPowerPhysicalAttack
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier
from dbz.util import dprint


TYPE = 'Drill'
NAME = 'Blue Reversal Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '133'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Blue'
RESTRICTED = False
CARD_TEXT = ('Do the exact same physical attack you defended against during your defending'
             ' round of combat, once per combat.')


class CardPowerPhysicalAttackBRD(CardPowerPhysicalAttack):
    def _get_card_power(self, player):
        if not player.opponent.card_powers_played_this_combat:
            return None
        card_power = player.opponent.card_powers_played_this_combat[-1]
        if not isinstance(card_power, CardPowerPhysicalAttack):
            return None
        card_power = card_power.copy()
        card_power.player = player

        # Ensure that the power is active and valid
        card_power.valid_from = None
        card_power.valid_until = None
        card_power.deactivated = False

        # No need to discard/remove the card because we do not control it
        card_power.discard_after_use = False
        card_power.remove_from_game_after_use = False

        # Without setting card to None, we can run into trouble when custom card_power logic checks
        # self.card then tries to manipulate it e.g. #25 Goku's Physical Attack, which attempts
        # to remove the card from the game.
        card_power.card = None

        # Do not modify how the power should be exhausted after use
        #card_power.exhaust_after_use = False
        #card_power.exhaust_until_next_turn_after_use = False

        # Regardless of how the copied card exhausts itself, make sure it's exhausted by next turn
        card_power.exhaust_after_this_turn()

        return card_power

    def is_restricted(self, player):
        card_power = self._get_card_power(player)
        # Ignore the copied card power's restrictions. If it was played last phase, it gets copied
        # and played this phase, regardless of its ordinary restrictions e.g. saiyan heritage only
        # Do check and pay for copied card's cost (if any) though
        if (not card_power
            or not player.can_afford_cost(card_power)):
            return True
        return super().is_restricted(player)

    def on_attack(self, player, phase):
        card_power = self._get_card_power(player)
        card_power = player.register_card_power(card_power)
        dprint(f'{self.player} copies {card_power} via {self.name}')
        dprint(f'  - {card_power.description}')

        # Log the copied card power (in case it needs to get copied again)
        self.player.card_powers_played_this_combat.append(card_power.copy())

        # Temporarily change the drill's damage attribute so damage estimate can be calculated
        self.damage = card_power.damage.copy()
        card_power.on_attack(player, phase)
        self.damage = Damage.none()

        # Need to also call on_resolved for the drill so it gets exhausted appropriately
        self.on_resolved()


CARD_POWER = CardPowerPhysicalAttackBRD(
    NAME, CARD_TEXT, exhaust_until_next_turn=True, discard=False, damage=Damage.none())
