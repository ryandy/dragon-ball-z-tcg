import sys

from exception import LossError
from personality_card import PersonalityCard
from pile import Pile


class Player:
    def __init__(self, deck):
        self.character = deck.cards[0].character
        self.personality_cards = []
        self.tokui_waza = None  # TODO

        life_deck_cards = []
        for card in deck.cards:
            if isinstance(card, PersonalityCard) and card.character == self.character:
                self.personality_cards.append(card)
            else:
                life_deck_cards.append(card)

        self.personality_cards.sort(key=lambda x: x.level)
        self.personality = self.personality_cards[0]
        self.personality.play_as_main()

        self.anger = 0
        self.opponent = None
        self.life_deck = Pile(life_deck_cards, shuffle=True)
        self.hand = Pile()
        self.discard_pile = Pile()
        self.removed_pile = Pile()
        self.allies = Pile()
        self.non_combat = Pile()
        self.drills = Pile()

    def __repr__(self):
        name = self.character.name.title()
        level = self.personality.level
        max_level = len(self.personality_cards)
        return f'{name} Lv{level}/{max_level} ({len(self.life_deck)} life)'

    def register_opponent(self, opponent):
        self.opponent = opponent

    def draw(self):
        card = self.life_deck.draw()
        self.hand.add(card)
        if len(self.life_deck) == 0:
            raise LossError('Life Deck is empty', self)

    def discard(self, idx):
        card = self.hand.remove(idx)
        self.discard_pile.add(card)

    def add_life_for_skipping_combat(self):
        card = self.discard_pile.draw()
        if card:
            self.life_deck.add_bottom(card)

    @staticmethod
    def show_pile(pile, detailed=False):
        for card in pile.cards:
            description = card.get_description(detailed=detailed)
            for line in description.split('\n'):
                print(f'  {line}')
            
    def show_hand(self, detailed=False):
        print(f'{len(self.hand)} card(s) in hand:')
        Player.show_pile(self.hand, detailed=detailed)

    def show_discard_pile(self, detailed=False):
        print(f'{len(self.discard_pile)} card(s) in discard pile:')
        Player.show_pile(self.discard_pile, detailed=detailed)

    def show_allies(self, detailed=False):
        if not self.allies.cards:
            print(f'No Allies')
        else:
            print(f'Allies:')
            Player.show_pile(self.allies, detailed=detailed)

    def show_personality(self, detailed=False):
        description = self.personality.get_description(
            detailed=True, anger=self.anger, life=len(self.life_deck))
        for line in description.split('\n'):
            print(f'{line}')

    def show(self, detailed=False):
        self.show_personality(detailed=detailed)
        self.show_hand(detailed=detailed)
        self.show_discard_pile(detailed=detailed)
