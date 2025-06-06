import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerNonCombatAttack
from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerAnyDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier
from dbz.state import State


TYPE = 'Combat'
NAME = 'Gohan\'s Father Save'
SUBTYPE = 'Combat - Attack'  # Must be used as an attack according to 11/24/04 CRD pg3
SAGA = 'Saiyan'
CARD_NUMBER = '214'
RARITY = 5
DECK_LIMIT = None
CHARACTER = 'Gohan'
STYLE = None
CARD_TEXT = ('If Gohan is Goku\'s ally, he stops the foe\'s combat turn.')


class CardPowerNonCombatAttackGFS(CardPowerNonCombatAttack):
    def is_restricted(self, player):
        if player.main_personality.character != Character.GOKU:  # Goku must be MP
            return True
        if not player.character_in_play(Character.GOHAN):  # Gohan must be an ally
            return True
        if State.TURN_PLAYER is player:  # Must be opponent's turn
            return True
        return super().is_restricted(player)


CARD_POWER = CardPowerNonCombatAttackGFS(
    NAME, CARD_TEXT, force_end_combat=True)
