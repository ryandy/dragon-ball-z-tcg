import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier
from dbz.drill_card import DrillCard


TYPE = 'Non-Combat'
NAME = 'Bulma Finds a Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '223'
RARITY = 5
DECK_LIMIT = None
CHARACTER = 'Bulma'
STYLE = None
CARD_TEXT = ('When the Bulma ally is in play, pick a drill from the life deck or discard pile'
             ' and put it into play.')


class CardPowerNonCombatAttackBFAD(CardPowerNonCombatAttack):
    def is_restricted(self, player):
        if not player.character_in_play(Character.BULMA, either_side=True, skip_main=True):
            return True
        return super().is_restricted(player)

    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)

        cards, names, descriptions = [], [], []
        for card in (player.life_deck + player.discard_pile):
            if (isinstance(card, DrillCard)
                and card.can_be_played(player)):
                cards.append(card)
                names.append(f'{card.name} ({card.pile.name})')
                descriptions.append(card.card_text)
        if cards:
            idx = player.choose(names, descriptions, allow_pass=False,
                                prompt='Select a Drill to play')
            drill = cards[idx]
            player.play_drill(drill)

        # Regardless of outcome, shuffle the deck after "searching" it
        player.shuffle_deck()


CARD_POWER = CardPowerNonCombatAttackBFAD(NAME, CARD_TEXT)
