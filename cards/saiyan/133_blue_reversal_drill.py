import sys

from card_power_attack import CardPowerPhysicalAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier
from util import dprint


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
        card_power.valid_from = None
        card_power.valid_until = None
        card_power.deactivated = False
        card_power.card = None
        card_power.discard = False
        card_power.remove_from_game = False

        # Regardless of how the copied card exhausts itself, make sure it's exhausted by next turn
        card_power.exhaust_after_this_turn()

        return card_power

    def is_restricted(self, player):
        card_power = self._get_card_power(player)
        if (not card_power
            or card_power.is_restricted(player)
            or not card_power.cost.can_afford(player, card_power)):
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
