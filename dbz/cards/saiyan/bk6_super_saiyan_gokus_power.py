import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Super Saiyan Goku\'s Power'
SAGA = 'Saiyan'
CARD_NUMBER = 'BK6'
RARITY = 2
DECK_LIMIT = 1
CHARACTER = 'Goku'
STYLE = None
CARD_TEXT = ('Remove foe\'s ally of your choice from the game. Remove from the game after use.')


class CardPowerNonCombatAttackSSGP(CardPowerNonCombatAttack):
    def is_restricted(self, player):
        if len(player.opponent.allies) == 0:
            return True
        return super().is_restricted(player)

    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        cards = player.opponent.allies.cards
        if cards:
            idx = player.choose([x.name for x in cards],
                                [x.card_text for x in cards],
                                allow_pass=False,
                                prompt='Select an opponent\'s ally to remove from the game')
            player.opponent.discard(cards[idx], remove_from_game=True)


CARD_POWER = CardPowerNonCombatAttackSSGP(NAME, CARD_TEXT, remove_from_game=True)
