import sys

from card import Card
from style import Style


class DrillCard(Card):
    def __init__(self, name, saga, card_number, rarity, deck_limit, character, style,
                 card_text, card_power, restricted):
        super().__init__(name, saga, card_number, rarity, deck_limit, character, style,
                         card_text, card_power)
        self.restricted = Style[restricted.upper()] if restricted else False

    def __repr__(self):
        return f'{self.name} (Non-Combat)'

    def can_be_played(self, player):
        if self.style == Style.FREESTYLE:
            return True

        # Styled drills cannot be played if they are duplicates of a drill you have in
        # play, are a different style than a drill you have in play, or are restricted and
        # are the same style as any styled drill in play.
        dup_restricted = any(x.get_id() == self.get_id() for x in player.drills)
        style_restricted = any(x.style != self.style
                               for x in player.drills if x.style != Style.FREESTYLE)
        special_restricted = (
            self.restricted
            and (any(x.style == self.restricted
                     for x in player.drills + player.opponent.drills)))

        # Goku's Mixing Drill allows drills of multiple colors to be used at the same time
        if player.card_in_play('saiyan.231'):  # Goku's Mixing Drill
            style_restricted = False

        return (not dup_restricted
                and not style_restricted
                and not special_restricted)

    @classmethod
    def from_spec(cls, card_module):
        card = cls(
            card_module.NAME,
            card_module.SAGA,
            card_module.CARD_NUMBER,
            card_module.RARITY,
            card_module.DECK_LIMIT,
            card_module.CHARACTER,
            card_module.STYLE,
            card_module.CARD_TEXT,
            card_module.CARD_POWER,
            card_module.RESTRICTED)
        for card_power in card.card_powers:
            card_power.register_card(card)
        return card
