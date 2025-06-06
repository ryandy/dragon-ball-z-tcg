import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'The Untroubled Mind is Focused'
SAGA = 'Saiyan'
CARD_NUMBER = '32'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Remove someone else\'s drill card or ally from the game. Remove from the game'
             ' after use.')


class CardPowerTUMIF(CardPowerNonCombatAttack):
    def is_restricted(self, player):
        if len(player.opponent.drills + player.opponent.allies) == 0:
            return True
        return super().is_restricted(player)

    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        cards = player.opponent.drills + player.opponent.allies
        if cards:
            idx = player.choose([x.name for x in cards],
                                [x.card_text for x in cards],
                                allow_pass=False,
                                prompt='Select an opponent\'s card to remove from the game')
            player.opponent.discard(cards[idx], remove_from_game=True)


CARD_POWER = CardPowerTUMIF(NAME, CARD_TEXT)
