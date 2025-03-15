import sys

from personality_card import PersonalityCard
from pile import Pile


class Player:
    def __init__(self, deck):
        # TODO: tokui-waza
        self.main_personality = deck.cards[0].character
        self.main_personality_cards = []
        self.main_personality_level = 1
        self.anger = 0
        self.power_stage = 5

        life_deck_cards = []
        for card in deck.cards:
            if isinstance(card, PersonalityCard) and card.character == self.main_personality:
                self.main_personality_cards.append(card)
            else:
                life_deck_cards.append(card)

        self.main_personality_cards.sort(key=lambda x: x.level)
        self.life_deck = Pile(life_deck_cards)
        self.hand = Pile()
        self.discard = Pile()
        self.allies = Pile()
        self.non_combat = Pile()
        self.drills = Pile()  # Does this need to be separate from non-combat?

    def __repr__(self):
        personality = self.main_personality.name.title()
        level = self.main_personality_level
        max_level = len(self.main_personality_cards)
        return f'{personality} Lv{level}/{max_level} ({len(self.life_deck)} life)'
