import sys

from dbz.card_power_on_attack_resolved import CardPowerOnAttackResolved
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Red Life Attack Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '232'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Red'
RESTRICTED = False
CARD_TEXT = ('Do an extra life card of damage whenever successful damage is done.')


class CardPowerOnAttackResolvedBTD(CardPowerOnAttackResolved):
    def on_condition(self, phase, damage, is_physical):
        return (self.player is phase.player  # attacking
                and not damage.was_stopped()  # successful
                and (damage.power > 0 or damage.life > 0))  # did damage

    # Unblockable 1 life damage
    def on_effect(self, phase, damage, is_physical):
        self.player.opponent.apply_life_damage(1)


CARD_POWER = CardPowerOnAttackResolvedBTD(
    NAME, CARD_TEXT, exhaust=False, discard=False, choice=False)
