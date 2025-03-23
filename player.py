import random
import sys

from card_power_attack import CardPowerAttack
from card_power_defense import CardPowerDefense
from character import Character
from combat_card import CombatCard
from dragon_ball_card import DragonBallCard
from drill_card import DrillCard
from exception import GameOver
from non_combat_card import NonCombatCard
from personality_card import PersonalityCard
from pile import Pile
from state import State
from style import Style
from util import dprint


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
        self.life_deck = Pile('LifeDeck', life_deck_cards, shuffle=True)
        for card in self.life_deck:
            card.set_pile(self.life_deck)

        self.hand = Pile('Hand')
        self.discard_pile = Pile('Discard')
        self.removed_pile = Pile('Removed')
        self.allies = Pile('Allies')
        self.non_combat = Pile('Non-Combat')
        self.drills = Pile('Drills')
        self.dragon_balls = Pile('DragonBalls')

        self.personality = self.personality_cards[0]
        self.personality.init_power_stage_for_main()
        self.register_card_powers(self.personality.card_powers)
        self.interactive = (self.name() == 'Goku') if State.ENABLE_INTERACTIVE else False

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
        card_power_copy = card_power.copy()
        card_power_copy.register_player(self)
        self.card_powers.append(card_power_copy)

    def register_card_powers(self, card_powers):
        for card_power in card_powers:
            self.register_card_power(card_power)

    def exhaust_card(self, card):
        for idx in reversed(range(len(self.card_powers))):
            if self.card_powers[idx].card is card:
                del self.card_powers[idx]

    def exhaust_card_power(self, card_power):
        for idx in reversed(range(len(self.card_powers))):
            if self.card_powers[idx] is card_power:
                del self.card_powers[idx]

    def exhaust_expired_card_powers(self):
        for idx in reversed(range(len(self.card_powers))):
            if self.card_powers[idx].is_exhausted():
                del self.card_powers[idx]

    def get_valid_card_powers(self, card_power_type):
        filtered_card_powers = []
        for card_power in self.card_powers:
            if ((not card_power_type or isinstance(card_power, card_power_type))
                and not card_power.is_exhausted()
                and not card_power.is_personality_restricted(self.personality)
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
            dprint(f'{self.name()} levels up to Lv{next_level}!')
            self.exhaust_card(self.personality)
            self.personality = self.personality_cards[next_level_idx]
            self.register_card_powers(self.personality.card_powers)

            # Discard/exhaust all drills
            while len(self.drills) > 0:
                card = self.drills.cards[-1]
                self.discard(card)
        else:
            dprint(f'{self.name()} levels up, but stays at Lv{next_level-1}!')

        # Set power to maximum
        self.personality.set_power_stage_max()

        # Reset anger to 0 if anger reached the maximum
        if self.anger == MAX_ANGER:
            self.anger = 0

    def reduce_level(self):
        '''Can be caused by card effects'''
        next_level = self.personality.level - 1
        next_level_idx = next_level - 1

        # Downgrade personality if possible
        if next_level_idx >= 0:
            dprint(f'{self.name()} levels down to Lv{next_level}!')
            self.exhaust_card(self.personality)
            self.personality = self.personality_cards[next_level_idx]
            self.register_card_powers(self.personality.card_powers)

            # Discard/exhaust all drills
            while len(self.drills) > 0:
                card = self.drills.cards[-1]
                self.discard(card)

            # Reset power
            self.personality.init_power_stage_for_main()

    def adjust_anger(self, count):
        self.anger = max(0, min(MAX_ANGER, self.anger + count))
        if self.anger == MAX_ANGER:
            self.raise_level()

    def draw(self, dest_pile=None):
        '''Life Deck -> Hand/Discard'''
        if dest_pile is None:
            dest_pile = self.hand

        card = self.life_deck.draw()

        # Check for end-of-game conditions
        if len(self.life_deck) == 0:
            raise GameOver(f'{self.name()}\'s Life Deck is empty', self.opponent)
        if (dest_pile is self.discard_pile
            and isinstance(card, DragonBallCard)
            and all(isinstance(x, DragonBallCard) for x in self.life_deck)):
            raise GameOver(f'{self.name()} can take no more life damage', self.opponent)

        # Check if a dragon ball is being discarded directly from the life deck - recycle it
        if (dest_pile is self.discard_pile
            and isinstance(card, DragonBallCard)):
            card.set_pile(dest_pile)  # Temporarily move card so it can move back when recycled
            self.recycle_dragon_ball(card)
            return None

        # Check if an unplayable drill was drawn - can shuffle back into deck
        if (dest_pile is self.hand
            and isinstance(card, DrillCard)
            and card.style != Style.FREESTYLE
            and any(x.style != card.style for x in self.drills if x.style != Style.FREESTYLE)):
            idx = 0
            if self.interactive:
                dprint(f'{self.name()} draws unplayable {card.name}')
                idx = self.choose(['Shuffle it back into deck.', 'Keep it.']
                                  ['', ''],
                                  allow_pass=False)
            if idx == 0:
                dprint(f'{self.name()} shuffles unplayable {card.name} back into deck')
                self.life_deck.add(card)
                self.life_deck.shuffle()
            return None

        # Adding cards to hand requires some special handling
        if dest_pile is self.hand:
            self.add_card_to_hand(card)
        else:
            dest_pile.add(card)
            card.set_pile(dest_pile)

        return card

    def add_card_to_hand(self, card):
        # Register callbacks for all new combat cards in hand
        if self.interactive:
            dprint(f'{self.name()} adds {card} to hand')
        else:
            dprint(f'{self.name()} adds a card to hand')
        self.hand.add(card)
        card.set_pile(self.hand)
        if (isinstance(card, CombatCard)
            or card.get_id() == 'saiyan.187'  # dragon ball that can be played as attack from hand
            ):
            for card_power in card.card_powers:
                if (isinstance(card_power, CardPowerAttack)
                    or isinstance(card_power, CardPowerDefense)):
                    self.register_card_power(card_power)

    def remove_from_game(self, card, exhaust_card=True):
        return self.discard(card, remove_from_game=True, exhaust_card=exhaust_card)

    def discard(self, card, remove_from_game=False, exhaust_card=True):
        '''Hand/Table -> Discard/Removed'''
        assert card.pile is not self.discard_pile and card.pile is not self.removed_pile

        card_removed = card.pile.remove(card)
        if card_removed is not card:
            print(f'Attempted to remove {card} from {card.pile} but got {card_removed}')
            assert False

        if exhaust_card:
            self.exhaust_card(card=card)

        if isinstance(card, DragonBallCard):
            self.recycle_dragon_ball(card)
        elif remove_from_game:
            dprint(f'{self.name()} removes {card} from game')
            self.removed_pile.add(card)
            card.set_pile(self.removed_pile)
        else:  # discard
            dprint(f'{self.name()} discards {card}')
            self.discard_pile.add(card)
            card.set_pile(self.discard_pile)

    def recycle_dragon_ball(self, card):
        dprint(f'{self.name()} recycles {card}')
        self.life_deck.add_bottom(card)
        card.set_pile(self.life_deck)

    def rejuvenate(self):
        card = self.discard_pile.remove_top()
        dprint(f'{self.name()} rejuvenates with {card}')
        if card:
            self.life_deck.add_bottom(card)
            card.set_pile(self.life_deck)

    def apply_physical_attack_damage(self, damage):
        damage = damage.resolve(self.opponent)
        dprint(f'{self.name()} takes {damage}')
        self.apply_power_damage(damage.power)
        self.apply_life_damage(damage.life)

    def apply_energy_attack_damage(self, damage):
        damage = damage.resolve(self.opponent)
        dprint(f'{self.name()} takes {damage}')
        self.apply_power_damage(damage.power)
        self.apply_life_damage(damage.life)

    def apply_power_damage(self, power_damage):
        life_damage = max(0, power_damage - self.personality.power_stage)
        self.personality.reduce_power_stage(power_damage)
        self.apply_life_damage(life_damage)

    def apply_life_damage(self, life_damage):
        discard_count = 0
        while discard_count < life_damage:
            card_discarded = self.draw(dest_pile=self.discard_pile)
            if card_discarded:
                discard_count += 1
                dprint(f'{self.name()} takes 1 life damage: {card_discarded}')

    def show_summary(self):
        '''1-line summary of current state'''
        name = self.name()
        level = self.personality.level
        anger = self.anger
        level = f'Lv{level}.{anger}'

        life = len(self.life_deck)
        allies = len(self.allies)
        discard = len(self.discard_pile)
        non_combat = len(self.non_combat)
        drills = len(self.drills)
        dbs = len(self.dragon_balls)
        hand = len(self.hand)

        power = self.personality.power_stage
        pat_idx = self.personality.get_physical_attack_table_index()
        power = f'{power}({pat_idx})'
        dprint(f'{level : <5} {name : <9} {life : >2}hp {discard : >2}dp {power : >5}pwr'
               f' {allies : >2}al {dbs : >2}db {drills : >2}dr {non_combat : >2}nc {hand : >2}hd')

    def choose(self, names, descriptions,
               other_names=None, other_descriptions=None,
               allow_pass=True):
        full_names = list(names)
        full_descriptions = list(descriptions)

        other_names = other_names or []
        if other_names:
            full_names.extend(other_names)
            full_descriptions.extend(other_descriptions)

        if allow_pass:
            full_names.append('Pass')
            full_descriptions.append('Do nothing.')

        dprint(f'>>> Choose an action:')

        show_descriptions = any(x for x in full_descriptions)
        for i in range(len(full_names)):
            if i < len(names):
                number = f'{i+1}'
            elif i < len(names) + len(other_names):
                number = f'/'
            else:  # pass
                number = f'{len(names)+1}'
            prefix = f'{number}. '
            dprint(f'{prefix}{full_names[i]}')
            if show_descriptions:
                dprint(f'{" "*(len(prefix)+2)}{full_descriptions[i]}')

        choice = -1
        while (choice < 0
               or choice >= len(names)+int(allow_pass)):
            choice = input('>>> Choice: ')
            try:
                choice = int(choice) - 1
            except:
                choice = -1

        # Check to see if 'Pass' (None) was chosen
        if allow_pass and choice == len(names):
            return None

        return choice

    def choose_card_power(self, card_power_type):
        # Random choice / UI choice / Heuristic choice

        filtered = self.get_valid_card_powers(card_power_type)

        if self.interactive:
            other_hand = []
            for card in self.hand:
                if not any(x.card is card for x in filtered):
                    other_hand.append(card)
            idx = self.choose(
                [str(cp) for cp in filtered],
                [cp.description for cp in filtered],
                other_names=[c.name for c in other_hand],
                other_descriptions=[c.card_text for c in other_hand])
        else:
            idx = random.randrange(len(filtered)) if filtered else None

        if idx is None:  # Pass
            return None
        return filtered[idx]

    def choose_discard_pile_card(self):
        if self.interactive:
            idx = self.choose(
                [str(c) for c in self.discard_pile],
                [c.card_text for c in self.discard_pile])
        else:
            idx = random.randrange(len(self.discard_pile)) if self.discard_pile.cards else None

        if idx is None:  # Pass
            return None
        return self.discard_pile.cards[idx]

    def choose_hand_non_combat_card(self):
        filtered = []
        for card in self.hand:
            if (isinstance(card, NonCombatCard)
                or isinstance(card, DragonBallCard)
                or (isinstance(card, DrillCard) and card.style == Style.FREESTYLE)):
                filtered.append(card)
            elif isinstance(card, DrillCard):
                dup_restricted = any(x.get_id() == card.get_id() for x in self.drills)
                style_restricted = any(x.style != card.style
                                       for x in self.drills if x.style != Style.FREESTYLE)
                special_restricted = (
                    card.restricted
                    and (any(x.style == card.style for x in self.drills)
                         or any(x.style == card.style for x in self.opponent.drills)))
                if (not dup_restricted
                    and not style_restricted
                    and not special_restricted):
                    filtered.append(card)

        if self.interactive:
            other_hand = []
            for card in self.hand:
                if not any(x is card for x in filtered):
                    other_hand.append(card)
            idx = self.choose(
                [str(c) for c in filtered],
                [c.card_text for c in filtered],
                other_names=[c.name for c in other_hand],
                other_descriptions=[c.card_text for c in other_hand])
        else:
            # May want to sometimes hold on to non-combat cards
            idx = random.randrange(len(filtered)) if (filtered and random.random() < 0.9) else None

        if idx is None:  # Pass
            return None
        return filtered[idx]

    def choose_hand_discard_card(self):
        '''Assumes hand has at least 1 card and a card must be chosen'''
        if self.interactive:
            idx = self.choose(
                [str(c) for c in self.hand],
                [c.card_text for c in self.hand],
                allow_pass=False)
        else:
            idx = random.randrange(len(self.hand))

        return self.hand.cards[idx]

    def choose_declare_combat(self):
        '''True -> declare combat'''
        if self.interactive:
            idx = self.choose(['Declare Combat', 'Skip Combat'],
                              ['', ''],
                              allow_pass=False)
        else:
            idx = 0 if random.random() < 0.9 else 1

        return idx == 0

    def play_non_combat_card(self, card):
        self.hand.remove(card)

        dprint(f'{self.name()} plays {card}')
        if not self.interactive:
            dprint(f'  - {card.card_text}')

        if isinstance(card, NonCombatCard):
            self.non_combat.add(card)
            card.set_pile(self.non_combat)
            for card_power in card.card_powers:
                self.register_card_power(card_power)
        elif isinstance(card, DrillCard):
            self.drills.add(card)
            card.set_pile(self.drills)

            # Discard any newly invalidated restricted drills
            for player in [self, self.opponent]:
                for drill_card in player.drills:
                    if (drill_card is not card
                        and drill_card.restricted
                        and drill_card.style == card.style):
                        dprint(f'{player.name()}\'s restricted {drill_card.name} invalidated')
                        player.discard(drill_card)

            for card_power in card.card_powers:
                self.register_card_power(card_power)
        elif isinstance(card, DragonBallCard):
            self.dragon_balls.add(card)
            card.set_pile(self.dragon_balls)
        else:
            assert False

        return card
