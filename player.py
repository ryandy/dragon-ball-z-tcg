import sys

from exception import GameOver
from personality_card import PersonalityCard
from pile import Pile


MAX_ANGER = 5


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
        self.personality.init_power_stage_for_main()

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
        name = self.name()
        level = self.personality.level
        max_level = len(self.personality_cards)
        return f'{name} Lv{level}/{max_level} ({len(self.life_deck)} life)'

    def name(self):
        return self.character.name.title()

    def register_opponent(self, opponent):
        self.opponent = opponent

    def raise_level(self):
        next_level = self.personality.level + 1
        next_level_idx = next_level - 1
        if (next_level_idx == len(self.personality_cards) - 1
            and len(self.personality_cards) >= len(self.opponent.personality_cards)):
            raise GameOver(f'{self.name()} has achieved the Most Powerful Personality', self)
        if next_level_idx < len(self.personality_cards):
            self.personality = self.personality_cards[next_level_idx]
        self.personality.init_power_stage_for_main()
        self.anger = 0

    def raise_anger(self, count):
        self.anger = min(self.anger + count, MAX_ANGER)
        if self.anger == MAX_ANGER:
            self.raise_level()

    def draw(self):
        card = self.life_deck.draw()
        self.hand.add(card)
        if len(self.life_deck) == 0:
            raise GameOver(f'{self.name()}\'s Life Deck is empty', self.opponent)

    def discard(self, idx):
        card = self.hand.remove(idx)
        self.discard_pile.add(card)

    def add_life_for_skipping_combat(self):
        card = self.discard_pile.draw()
        if card:
            self.life_deck.add_bottom(card)

    def apply_physical_damage(self, damage):
        energy_damage = max(0, damage - self.personality.power_stage)
        self.personality.reduce_power_stage(damage)
        self.apply_energy_damage(energy_damage)

    def apply_energy_damage(self, damage):
        for _ in range(damage):
            card = self.draw()
            self.discard_pile.add(card)

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
        #self.show_discard_pile(detailed=detailed)
