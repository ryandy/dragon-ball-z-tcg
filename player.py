import random
import sys

from exception import GameOver
from personality_card import PersonalityCard
from pile import Pile


MAX_ANGER = 5


class Player:
    def __init__(self, deck, state):
        self.state = state
        self.character = deck.cards[0].character
        self.personality_cards = []
        self.tokui_waza = None  # TODO
        self.card_powers = []
        self.anger = 0
        self.opponent = None

        life_deck_cards = []
        for card in deck.cards:
            if isinstance(card, PersonalityCard) and card.character == self.character:
                self.personality_cards.append(card)
            else:
                life_deck_cards.append(card)

        self.personality_cards.sort(key=lambda x: x.level)
        self.life_deck = Pile(life_deck_cards, shuffle=True)

        self.hand = Pile()
        self.discard_pile = Pile()
        self.removed_pile = Pile()
        self.allies = Pile()
        self.non_combat = Pile()
        self.drills = Pile()

        self.personality = self.personality_cards[0]
        self.personality.init_power_stage_for_main()
        self.register_card_powers(self.personality.card_powers)

    def __repr__(self):
        name = self.name()
        level = self.personality.level
        max_level = len(self.personality_cards)
        life = len(self.life_deck)
        non_combat = len(self.allies) + len(self.non_combat) + len(self.drills)
        anger = self.anger
        hand = len(self.hand)
        power = self.personality.power_stage
        pat_idx = self.personality.get_physical_attack_table_index()
        return f'{name} (v{level}.{anger}/{life}hp/{power}pow/{pat_idx}atk/{non_combat}nc/{hand}c)'

    def name(self):
        return self.character.name.title()

    def register_opponent(self, opponent):
        self.opponent = opponent

    def register_card_power(self, card_power):
        self.card_powers.append(card_power)

    def register_card_powers(self, card_powers):
        self.card_powers.extend(card_powers)

    def exhaust_card(self, card):
        for idx in reversed(range(len(self.card_powers))):
            if self.card_powers[idx].card is card:
                del self.card_powers[idx]

    def exhaust_card_power(self, card_power):
        for idx in reversed(range(len(self.card_powers))):
            if self.card_powers[idx] is card_power:
                del self.card_powers[idx]

    def exhaust_card_powers(self, card_powers):
        for card_power in card_powers:
            self.exhaust_card_power(card_power)

    def exhaust_expired_card_powers(self):
        for idx in reversed(range(len(self.card_powers))):
            if self.card_powers[idx].is_exhausted():
                del self.card_powers[idx]

    def get_valid_card_powers(self, card_power_type):
        filtered_card_powers = []
        for card_power in self.card_powers:
            if ((not card_power_type or isinstance(card_power, card_power_type))
                and not card_power.is_exhausted()
                and self.can_afford_cost(card_power.cost)):
                filtered_card_powers.append(card_power)
        return filtered_card_powers

    def can_afford_cost(self, cost):
        return (self.personality.power_stage >= cost.power
                and len(self.life_deck) >= cost.life)

    def pay_cost(self, cost):
        assert self.can_afford_cost(cost)
        self.personality.reduce_power_stage(cost.power)
        self.apply_life_damage(cost.life)

    def raise_level(self):
        next_level = self.personality.level + 1
        next_level_idx = next_level - 1

        # Check for win condition
        if (next_level_idx == len(self.personality_cards) - 1
            and len(self.personality_cards) >= len(self.opponent.personality_cards)):
            raise GameOver(f'{self.name()} has achieved the Most Powerful Personality', self)

        # Upgrade personality if possible
        if next_level_idx < len(self.personality_cards):
            self.exhaust_card(self.personality)
            self.personality = self.personality_cards[next_level_idx]
            self.register_card_powers(self.personality.card_powers)

            # Discard all drills
            while len(self.drills) > 0:
                card = self.drills.draw()
                self.discard_pile.add(card)

        # Set power to maximum
        self.personality.init_power_stage_for_main()

        # Reset anger to 0
        self.anger = 0

    def adjust_anger(self, count):
        self.anger = max(0, min(MAX_ANGER, self.anger + count))
        if self.anger == MAX_ANGER:
            self.raise_level()

    def draw(self, dest_pile=None):
        if dest_pile is None:
            dest_pile = self.hand
        card = self.life_deck.draw()
        dest_pile.add(card)
        if len(self.life_deck) == 0:
            raise GameOver(f'{self.name()}\'s Life Deck is empty', self.opponent)
        return card

    def discard(self, card_or_idx):
        # TODO: Prevent discarding dragon balls (dragon balls do not count toward damage)
        card = self.hand.remove(card_or_idx)
        assert card
        self.exhaust_card(card=card)
        self.discard_pile.add(card)

    def rejuvenate(self):
        card = self.discard_pile.draw()
        if card:
            self.life_deck.add_bottom(card)

    def apply_physical_attack_damage(self, damage):
        damage = damage.resolve(self.opponent)
        self.apply_power_damage(damage.power)
        self.apply_life_damage(damage.life)

    def apply_energy_attack_damage(self, damage):
        damage = damage.resolve(self.opponent)
        self.apply_power_damage(damage.power)
        self.apply_life_damage(damage.life)

    def apply_power_damage(self, power_damage):
        life_damage = max(0, power_damage - self.personality.power_stage)
        self.personality.reduce_power_stage(power_damage)
        self.apply_life_damage(life_damage)

    def apply_life_damage(self, life_damage):
        for _ in range(life_damage):
            self.draw(dest_pile=self.discard_pile)

    @staticmethod
    def show_pile(pile, detailed=False):
        for card in pile.cards:
            description = card.get_description(detailed=detailed)
            for line in description.split('\n'):
                print(f'  {line}')
            
    def show_hand(self, detailed=False):
        print(f'{len(self.hand)} card(s) in {self.name()}\'s hand:')
        Player.show_pile(self.hand, detailed=detailed)

    def show_discard_pile(self, detailed=False):
        print(f'{len(self.discard_pile)} card(s) in {self.name()}\'s discard pile:')
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

    def card_power_choice(self, card_power_type):
        # Filter
        # Random choice / UI choice / Heuristic choice

        # TODO: for UI, will want to display valid-ish card powers e.g. cannot afford
        filtered = self.get_valid_card_powers(card_power_type)

        #print(f'{self} has {len(filtered)} {card_power_type.__name__} choice(s)')
        #if card_power_type is CardPowerEnergyDefense:
        #    for card_power in filtered:
        #        print(f'  {card_power.name}')
        #    print(f'  Cards in hand:')
        #    for card in self.hand:
        #        print(f'    {card}')

        if not filtered:
            return None

        idx = random.randrange(len(filtered))
        return filtered[idx]
