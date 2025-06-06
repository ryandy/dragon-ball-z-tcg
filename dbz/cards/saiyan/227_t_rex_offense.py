import sys

from dbz.card_power_on_attack_resolved import CardPowerOnAttackResolved
from dbz.card_power_on_damage_modification import CardPowerOnDamageModification
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier
from dbz.state import State
from dbz.util import dprint


TYPE = 'Non-Combat'
NAME = 'T-Rex Offense'
SAGA = 'Saiyan'
CARD_NUMBER = '227'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Use when you perform an energy attack to have that energy attack do an additional'
             ' +1 life cards of damage. If a successful energy attack is performed against you'
             ' while this card in play, this card is discarded.')


class CardPowerOnDamageModificationTRO(CardPowerOnDamageModification):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._choice = False
        self._choice_time = (-1, -1)

    def on_energy_damage_modification(self, attacker, phase):
        mod = super().on_energy_damage_modification(attacker, phase)
        if not mod:
            return

        if self._choice_time != State.get_time():
            self._choice_time = State.get_time()
            self._choice = self.player.choose_to_use_card_power(self)
            if self._choice:
                dprint(f'{self.player} uses {self}')
                dprint(f'  - {self.description}')
                self.exhaust_after_this_combat_attack_phase()
                if self.card:
                    self.player.discard(self.card, exhaust_card=False)

        if self._choice:
            return mod


class CardPowerOnAttackResolvedTRO(CardPowerOnAttackResolved):
    def on_condition(self, phase, damage, is_physical):
        return (self.player is not phase.player  # opp attacking
                and not damage.was_stopped()  # successful
                and not is_physical)  # energy

    def on_effect(self, phase, damage, is_physical):
        # Discard and exhaust all related card powers (handled by on_resolved)
        if self.card and self.card.pile is self.player.non_combat:
            self.discard_after_use = True


CARD_POWER = [
    CardPowerOnDamageModificationTRO(
        NAME, CARD_TEXT, own_energy=DamageModifier(life_add=1)),
    CardPowerOnAttackResolvedTRO(
        NAME, CARD_TEXT, exhaust=True, discard=False, silent=True)
]
