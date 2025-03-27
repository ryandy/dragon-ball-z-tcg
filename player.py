import collections
import random
import sys

from card import Card
from card_power import CardPower
from card_power_attack import CardPowerAttack
from card_power_defense import CardPowerDefense
from card_power_defense_shield import (CardPowerPhysicalDefenseShield,
                                       CardPowerEnergyDefenseShield,
                                       CardPowerAnyDefenseShield)
from card_power_dragon_ball import CardPowerDragonBall
from card_power_on_remove_from_play import CardPowerOnRemoveFromPlay
from character import Character
from combat_card import CombatCard
from deck import Deck
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
    def __init__(self, deck, state, interactive=False):
        self.state = state
        self.interactive = interactive
        self.character = deck.cards[0].character
        self.main_personalities = []
        self.main_personality = None
        self.control_personality = None
        self.tokui_waza = None  # TODO
        self.card_powers = []
        self.anger = 0
        self.opponent = None

        life_deck_cards = []
        for card in deck.cards:
            card.register_owner(self)
            if isinstance(card, PersonalityCard) and card.character == self.character:
                self.main_personalities.append(card)
            else:
                life_deck_cards.append(card)

        self.main_personalities.sort(key=lambda x: x.level)
        self.life_deck = Deck('LifeDeck', life_deck_cards)
        self.life_deck.shuffle()
        for card in self.life_deck:
            card.set_pile(self.life_deck)

        self.hand = Pile('Hand')
        self.discard_pile = Pile('Discard')
        self.removed_pile = Pile('Removed')
        self.allies = Pile('Allies')
        self.non_combat = Pile('Non-Combat')
        self.drills = Pile('Drills')
        self.dragon_balls = Pile('DragonBalls')

        self.main_personality = self.main_personalities[0]
        self.main_personality.init_for_main()
        self.control_personality = self.main_personality
        self.register_card_powers(self.main_personality.card_powers)
        self.name = self.main_personality.char_name()

    def __repr__(self):
        if self.control_personality is not self.main_personality:
            return f'{self.name}/{self.control_personality.char_name()}'
        return self.name

    def debug(self):
        '''Use to jump into the game at certain points to debug'''
        self.interactive = True
        State.INTERACTIVE = True

    def register_opponent(self, opponent):
        self.opponent = opponent

    def register_card_power(self, card_power):
        card_power_copy = card_power.copy()
        card_power_copy.register_player(self)
        self.card_powers.append(card_power_copy)

    def register_card_powers(self, card_powers):
        for card_power in card_powers:
            self.register_card_power(card_power)

    def activate_card_powers(self, card):
        for card_power in self.card_powers:
            if card_power.card is card:
                card_power.activate()

    def deactivate_card_powers(self, card):
        for card_power in self.card_powers:
            if card_power.card is card:
                card_power.deactivate()

    def exhaust_card(self, card):
        for idx in reversed(range(len(self.card_powers))):
            if self.card_powers[idx].card is card:
                del self.card_powers[idx]

    def exhaust_card_until_next_turn(self, card):
        for idx in reversed(range(len(self.card_powers))):
            if self.card_powers[idx].card is card:
                self.card_powers[idx].exhaust_until_next_turn()

    def exhaust_card_power(self, card_power):
        for idx in reversed(range(len(self.card_powers))):
            if self.card_powers[idx] is card_power:
                del self.card_powers[idx]

    def exhaust_expired_card_powers(self):
        for idx in reversed(range(len(self.card_powers))):
            if self.card_powers[idx].is_exhausted():
                del self.card_powers[idx]

    def get_valid_card_powers(self, card_power_types):
        if not isinstance(card_power_types, list):
            card_power_types = [card_power_types]

        filtered_card_powers = []
        for card_power in self.card_powers:
            if (any(isinstance(card_power, x) for x in card_power_types)
                and not card_power.is_exhausted()
                and not card_power.is_deactivated()
                and not card_power.is_restricted(self)
                and card_power.cost.can_afford(self)):
                filtered_card_powers.append(card_power)
        return filtered_card_powers

    def card_in_play(self, card_or_card_id, own_side=True, either_side=False):
        if isinstance(card_or_card_id, Card):
            card_id = card_or_card_id.get_id()
        else:
            card_id = card_or_card_id

        cards = []
        opp_side = not own_side or either_side
        own_side = own_side or either_side
        if own_side:
            cards += (self.allies.cards + self.non_combat.cards
                      + self.drills.cards + self.dragon_balls.cards)
        if opp_side:
            cards += (self.opponent.allies.cards + self.opponent.non_combat.cards
                      + self.opponent.drills.cards + self.opponent.dragon_balls.cards)
        for card in cards:
            if card.get_id() == card_id:
                return True
        return False

    def raise_level(self):
        next_level = self.main_personality.level + 1
        next_level_idx = next_level - 1

        # Check for win condition
        if (next_level_idx == len(self.main_personalities) - 1
            and len(self.main_personalities) >= len(self.opponent.main_personalities)):
            dprint(f'{self} levels up to Lv{next_level}!')
            raise GameOver(f'{self} has achieved the Most Powerful Personality', self)

        # Upgrade personality if possible
        if next_level_idx < len(self.main_personalities):
            dprint(f'{self} levels up to Lv{next_level}!')
            self.exhaust_card(self.main_personality)

            # Control personality only updates if it is currently MP
            if self.control_personality is self.main_personality:
                self.control_personality = self.main_personalities[next_level_idx]
            self.main_personality = self.main_personalities[next_level_idx]
            self.main_personality.init_for_main()

            # Register (and deactivate if not in control) new card powers
            self.register_card_powers(self.main_personality.card_powers)
            if self.control_personality is not self.main_personality:
                self.deactivate_card_powers(self.main_personality)

            # Discard/exhaust all drills
            while len(self.drills) > 0:
                card = self.drills.cards[-1]
                self.discard(card)
        else:
            dprint(f'{self} levels up, but stays at Lv{next_level-1}!')

        # Set power to maximum
        self.main_personality.set_power_stage_max()

        # Reset anger to 0 if anger reached the maximum
        if self.anger == MAX_ANGER:
            self.anger = 0

    def reduce_level(self):
        '''Can be caused by card effects'''
        next_level = self.main_personality.level - 1
        next_level_idx = next_level - 1

        # Downgrade personality if possible
        if next_level_idx < 0:
            return

        dprint(f'{self} levels down to Lv{next_level}!')
        self.exhaust_card(self.main_personality)

        # Control personality only updates if it is currently MP
        if self.control_personality is self.main_personality:
            self.control_personality = self.main_personalities[next_level_idx]
        self.main_personality = self.main_personalities[next_level_idx]

        # Register (and deactivate if not in control) new card powers
        self.register_card_powers(self.main_personality.card_powers)
        if self.control_personality is not self.main_personality:
            self.deactivate_card_powers(self.main_personality)

        # Discard/exhaust all drills
        while len(self.drills) > 0:
            card = self.drills.cards[-1]
            self.discard(card)

        # Reset power
        self.main_personality.init_for_main()

    def adjust_anger(self, count):
        new_anger = max(0, min(MAX_ANGER, self.anger + count))
        delta = new_anger - self.anger
        if delta:
            verb = 'increases' if delta > 0 else 'decreases'
            dprint(f'{self.name}\'s anger {verb} from {self.anger} to {new_anger}')

        self.anger = new_anger
        if self.anger == MAX_ANGER:
            self.raise_level()

    def check_for_dragon_ball_victory(self):
        set_counts = collections.defaultdict(int)
        for card in self.dragon_balls:
            set_counts[card.db_set] += 1
            if set_counts[card.db_set] == 7:
                raise GameOver(f'{self} has collected all 7 {card.db_set} Dragon Balls',self)

    def draw(self, card=None, dest_pile=None):
        '''Life Deck -> Hand/Discard'''
        if dest_pile is None:
            dest_pile = self.hand

        if card is None:
            card = self.life_deck.draw()

        # Check for end-of-game conditions
        if (dest_pile is self.discard_pile
            and isinstance(card, DragonBallCard)
            and all(isinstance(x, DragonBallCard) for x in self.life_deck)):
            raise GameOver(f'{self} can take no more life damage', self.opponent)

        # Check if a dragon ball is being discarded directly from the life deck - recycle it
        if (dest_pile is self.discard_pile
            and isinstance(card, DragonBallCard)):
            card.set_pile(None)  # Temporarily move card so it can move back when recycled
            self.recycle_dragon_ball(card)
            return None

        # Check if an unplayable drill was drawn to hand - can shuffle back into deck
        if (dest_pile is self.hand
            and isinstance(card, DrillCard)
            and card.style != Style.FREESTYLE
            and any(x.style != card.style for x in self.drills if x.style != Style.FREESTYLE)):
            if self.interactive:
                dprint(f'{self} draws unplayable {card.name}')
            idx = self.choose(['Shuffle it back into deck.', 'Keep it.'], [''],
                              allow_pass=False)
            if idx == 0:
                dprint(f'{self} shuffles unplayable {card.name} back into deck')
                self.life_deck.add(card)
                self.life_deck.shuffle()
                if card.pile is not self.life_deck:
                    card.set_pile(self.life_deck)
                return None

        # Adding cards to hand requires some special handling
        if dest_pile is self.hand:
            self.add_card_to_hand(card)
        else:
            dest_pile.add(card)
            card.set_pile(dest_pile)

        return card

    def add_card_to_hand(self, card):
        assert card
        if self.interactive:
            dprint(f'{self} adds {card} to hand')
        else:
            dprint(f'{self} adds a card to hand')
        self.hand.add(card)
        card.set_pile(self.hand)

        # Register callbacks for all new combat cards in hand
        if (isinstance(card, CombatCard)
            or card.get_id() == 'saiyan.187'  # dragon ball that can be played as attack from hand
            ):
            for card_power in card.card_powers:
                if (isinstance(card_power, CardPowerAttack)
                    or isinstance(card_power, CardPowerDefense)):
                    self.register_card_power(card_power)

    def remove_from_game(self, card, exhaust_card=True):
        return self.discard(card, remove_from_game=True, exhaust_card=exhaust_card)

    def discard_covered_allies(self, card, remove_from_game=False):
        covered_ally = card.covered_ally
        while covered_ally:
            self.discard(covered_ally, remove_from_game=remove_from_game, card_in_pile=False)
            covered_ally = covered_ally.covered_ally

    def discard(self, card, remove_from_game=False, exhaust_card=True, card_in_pile=True):
        '''Hand/Table -> Discard/Removed'''
        src_pile = card.pile

        if card_in_pile:
            if remove_from_game:
                assert card.pile is not self.removed_pile
            else:
                assert card.pile is not self.discard_pile

            card_removed = card.pile.remove(card)
            if card_removed is not card:
                print(f'Attempted to remove {card} from {card.pile} but got {card_removed}')
                assert False

        if exhaust_card:
            self.exhaust_card(card)

        if isinstance(card, DragonBallCard) and not remove_from_game:
            self.recycle_dragon_ball(card)
        elif remove_from_game:
            dprint(f'{self} removes {card} from game')
            self.removed_pile.add(card)
            card.set_pile(self.removed_pile)
        else:  # discard
            dprint(f'{self} discards {card}')
            self.discard_pile.add(card)
            card.set_pile(self.discard_pile)

        if (src_pile is self.allies
            or src_pile is self.non_combat
            or src_pile is self.drills):
            for card_power in card.card_powers:
                if isinstance(card_power, CardPowerOnRemoveFromPlay):
                    card_power.on_remove_from_play(self, State.PHASE)

        if isinstance(card, PersonalityCard) and src_pile is self.allies:
            self.discard_covered_allies(card, remove_from_game=remove_from_game)
            if self.control_personality is card:
                self.revert_control_of_combat()

    def recycle_dragon_ball(self, card):
        '''Card has already been removed from its source pile, so currently in no-mans-land'''
        dup_restricted = any(card.is_duplicate(x)
                             for x in self.dragon_balls + self.opponent.dragon_balls)
        if dup_restricted:
            # If this is a duplicate of a dragon ball in play, remove it from the game
            self.discard(card, remove_from_game=True, card_in_pile=False)
        else:
            dprint(f'{self} recycles {card}')
            self.life_deck.add_bottom(card)
            card.set_pile(self.life_deck)

    def steal_dragon_ball(self):
        card = self.choose_opponent_dragon_ball()
        if not card:
            return

        dprint(f'{self} steals {card.name}!')
        self.opponent.dragon_balls.remove(card)
        self.dragon_balls.add(card)
        card.set_pile(self.dragon_balls)

        for idx in reversed(range(len(self.opponent.card_powers))):
            if self.opponent.card_powers[idx].card is card:
                card_power = self.opponent.card_powers[idx]
                dprint(f'{self} takes over {card_power} card power')
                del self.opponent.card_powers[idx]
                self.register_card_power(card_power)

    def rejuvenate(self):
        card = self.discard_pile.remove_top()
        if card:
            dprint(f'{self} rejuvenates with {card}')
            self.life_deck.add_bottom(card)
            card.set_pile(self.life_deck)
        else:
            dprint(f'{self} failed to rejuvenate because the discard pile is empty')

    def _apply_damage(self, damage, src_personality=None, is_physical=None):
        damage = damage.resolve(self.opponent)
        dprint(f'{self} takes {damage}')

        carryover_life_damage = self.apply_power_damage(damage.power - damage.power_prevent)
        self.apply_life_damage(
            damage.life + carryover_life_damage - damage.life_prevent,
            src_personality=src_personality)

    def apply_physical_attack_damage(self, damage, src_personality=None):
        return self._apply_damage(damage, src_personality=src_personality, is_physical=True)

    def apply_energy_attack_damage(self, damage, src_personality=None):
        return self._apply_damage(damage, src_personality=src_personality, is_physical=False)

    def apply_power_damage(self, power_damage):
        '''Returns amount of excess damage that could not be applied to target personality'''
        if power_damage <= 0:
            return 0

        target_personality = self.choose_damage_target()
        if target_personality is not self.main_personality:
            dprint(f'{self} selects {target_personality.name} to take damage')

        carryover_life_damage = max(0, power_damage - target_personality.power_stage)
        power_damage -= carryover_life_damage
        dprint(f'{target_personality.name} takes {power_damage} power damage')
        target_personality.reduce_power_stage(power_damage)
        return carryover_life_damage

    def apply_life_damage(self, life_damage, src_personality=None):
        life_damage = max(0, life_damage)

        # Check for Dragon Ball Personality Capture
        if (0 < life_damage < 5
            and len(self.dragon_balls) > 0
            and src_personality
            and src_personality.character.can_steal_dragon_balls()):
            # Opponent can choose to steal or deal the damage
            dprint(f'{src_personality.char_name()} can steal a dragon ball instead of'
                   f' dealing {life_damage} life damage')
            idx = self.opponent.choose(
                ['Steal a Dragon Ball.'], ['Deal the damage.'], [''], allow_pass=False)
            if idx == 0:
                self.opponent.steal_dragon_ball()
                return

        discard_count = 0
        while discard_count < life_damage:
            card_discarded = self.draw(dest_pile=self.discard_pile)
            if card_discarded:
                discard_count += 1
                dprint(f'{self} takes 1 life damage: {card_discarded}')

        # Check for Dragon Ball Life Card Capture
        if discard_count >= 5 and src_personality:
            self.opponent.steal_dragon_ball()

    def determine_control_of_combat(self):
        if self.main_personality.power_stage < 2 and len(self.allies) > 0:
            dprint(f'{self.name} is weak and may select an ally to take control of Combat')

            new_control_personality = self.choose_personality()
            if self.control_personality is not new_control_personality:
                self.deactivate_card_powers(self.control_personality)
                self.control_personality = new_control_personality
                self.activate_card_powers(self.control_personality)

            if self.control_personality is self.main_personality:
                dprint(f'{self} has control of Combat')
            else:
                dprint(f'{self.control_personality.char_name()} takes control of Combat'
                       f' for {self.name}')

    def revert_control_of_combat(self):
        if self.control_personality is not self.main_personality:
            self.deactivate_card_powers(self.control_personality)
            dprint(f'{self.name} resumes control of Combat')
            self.control_personality = self.main_personality
            self.activate_card_powers(self.control_personality)

    def revert_control_of_combat_if_able(self):
        if self.main_personality.power_stage >= 2:
            self.revert_control_of_combat()

    def show_summary(self):
        '''1-line summary of current state'''
        level = f'Lv{self.main_personality.level}.{self.anger}'
        name = self.name
        power = self.main_personality.get_power_attack_str()
        life = len(self.life_deck)
        allies = len(self.allies)
        discard = len(self.discard_pile)
        non_combat = len(self.non_combat)
        drills = len(self.drills)
        dbs = len(self.dragon_balls)
        hand = len(self.hand)
        dprint(f'{level : <5} {name : <9} {power : >5}pwr {life : >2}hp {discard : >2}dp'
               f' {allies : >2}al {dbs : >2}db {drills : >2}dr {non_combat : >2}nc {hand : >2}hd')
        for ally in self.allies:
            level = f'Lv{ally.level}'
            name = ally.char_name()
            power = ally.get_power_attack_str()
            dprint(f'{level : <5} {name : <9} {power : >5}pwr')

    def choose(self, names, descriptions,
               other_names=None, other_descriptions=None,
               allow_pass=True, prompt=None):
        assert names or allow_pass

        if not self.interactive:
            if allow_pass and not names:  # Have to pass if that's the only option
                return None
            if allow_pass and random.random() < 0.1:  # Pass small % of the time
                return None
            return random.randrange(len(names))  # Random choice

        full_names = list(names)
        full_descriptions = list(descriptions)

        other_names = other_names or []
        if other_names:
            full_names.extend(other_names)
            full_descriptions.extend(other_descriptions)

        show_descriptions = any(x for x in full_descriptions)
        if allow_pass:
            full_names.append('Pass')
            full_descriptions.append('Do nothing.')

        prompt = prompt or 'Choose an action'
        dprint(f'>>> {prompt}:')
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

    def choose_card_power(self, card_power_type, prompt=None):
        filtered = self.get_valid_card_powers(card_power_type)

        other_hand = []
        for card in self.hand:
            if not any(x.card is card for x in filtered):
                other_hand.append(card)
        idx = self.choose(
            [str(cp) for cp in filtered],
            [cp.description for cp in filtered],
            other_names=[c.name for c in other_hand],
            other_descriptions=[c.card_text for c in other_hand],
            prompt=prompt)

        if idx is None:  # Pass
            return None
        return filtered[idx]

    def choose_defense_shield(self, is_physical=None):
        card_power_class = (CardPowerPhysicalDefenseShield
                            if is_physical else CardPowerEnergyDefenseShield)
        filtered = self.get_valid_card_powers(
            [card_power_class, CardPowerAnyDefenseShield])
        if not filtered:
            return None

        idx = self.choose(
            [str(cp) for cp in filtered],
            [cp.description for cp in filtered],
            allow_pass=False,
            prompt='Select a Defense Shield to activate')
        return filtered[idx]

    def choose_discard_pile_card(self):
        if len(self.discard_pile) == 0:
            return None

        idx = self.choose(
            [str(c) for c in self.discard_pile],
            [c.card_text for c in self.discard_pile])

        if idx is None:  # Pass
            return None
        return self.discard_pile.cards[idx]

    def choose_hand_discard_card(self):
        '''Assumes hand has at least 1 card and a card must be chosen'''
        idx = self.choose(
            [str(c) for c in self.hand],
            [c.card_text for c in self.hand],
            allow_pass=False)

        return self.hand.cards[idx]

    def choose_declare_combat(self):
        '''True -> declare combat'''
        idx = self.choose(['Declare Combat'], [''])

        if idx is None:
            return False
        return True

    def choose_to_use_card_power(self, card_power):
        idx = self.choose([f'Use {card_power}'], [card_power.description],
                          prompt=f'You can use {card_power} now')
        return idx == 0

    def choose_opponent_dragon_ball(self, prompt=None):
        if not self.opponent.dragon_balls.cards:
            return None

        if prompt is None:
            prompt = 'Select a Dragon Ball to steal'

        # Annotate choices with active card powers
        names, descriptions = [], []
        card_powers = self.opponent.get_valid_card_powers(CardPower)
        for card in self.opponent.dragon_balls:
            suffix = ' (*)' if any(x.card is card for x in card_powers) else ''
            if card.owner is not self.opponent:
                suffix = f' ({card.owner}\'s){suffix}'

            names.append(f'{card.name}{suffix}')
            descriptions.append(card.card_text)

        idx = self.choose(names, descriptions, allow_pass=False, prompt=prompt)
        return self.opponent.dragon_balls.cards[idx]

    def choose_damage_target(self):
        return self.choose_personality(
            prompt='Select a personality to take power stages of damage')

    def choose_power_stage_target(self, power):
        verb = 'gain' if power > 0 else 'lose'
        return self.choose_personality(
            prompt=f'Select a personality to {verb} {abs(power)} power stage(s)')

    def choose_personality(self, skip_main=False, prompt=None):
        if skip_main:
            assert len(self.allies) > 0

        if len(self.allies) == 0:
            return self.main_personality

        names, descriptions = [], []
        personalities = [] if skip_main else [self.main_personality]
        personalities.extend(self.allies.cards)
        prompt = prompt or 'Select a personality'
        for personality in personalities:
            level = (f'Lv{personality.level}.{self.anger}'
                     if personality is self.main_personality
                     else f'Lv{personality.level}')
            name = personality.char_name()
            power = personality.get_power_attack_str()
            card_power_available = any(
                x.card is personality and not x.is_floating and not x.is_exhausted()
                for x in self.card_powers)
            prefix = '' if card_power_available else '(/) '
            names.append(f'{level : <5} {name : <9} {power : >5}pwr')
            descriptions.append(f'{prefix}{personality.card_text}')

        idx = self.choose(names, descriptions, allow_pass=False, prompt=prompt)
        idx = idx + 1 if skip_main else idx
        if idx == 0:
            return self.main_personality
        return self.allies.cards[idx-1]

    def choose_hand_non_combat_card(self):
        filtered = []
        for card in self.hand:
            if (isinstance(card, NonCombatCard)
                or isinstance(card, DrillCard)
                or isinstance(card, DragonBallCard)
                or isinstance(card, PersonalityCard)):
                if card.can_be_played(self):
                    filtered.append(card)

        other_hand = []
        for card in self.hand:
            if not any(x is card for x in filtered):
                other_hand.append(card)

        idx = self.choose(
            [str(c) for c in filtered],
            [c.card_text for c in filtered],
            other_names=[c.name for c in other_hand],
            other_descriptions=[c.card_text for c in other_hand],
            prompt='Select a Non-Combat card to play from your hand')

        if idx is None:  # Pass
            return None
        return filtered[idx]

    def play_ally(self, card):
        dprint(f'{self} plays {card}')
        if not self.interactive:
            dprint(f'  - {card.card_text}')

        # TODO: Saibaimen can choose whether/which to overlay
        covered_ally = None
        for ally in self.allies:
            if ally.character == card.character and ally.level == card.level - 1:
                assert covered_ally is None
                covered_ally = ally

        card.init_for_ally(covered_ally=covered_ally)
        if covered_ally:
            self.exhaust_card(covered_ally)
            self.allies.remove(covered_ally)

        card.pile.remove(card)
        self.allies.add(card)
        card.set_pile(self.allies)

        for card_power in card.card_powers:
            self.register_card_power(card_power)
        self.deactivate_card_powers(card)  # Card powers deactivated until they take over combat

    def play_drill(self, card):
        dprint(f'{self} plays {card}')
        if not self.interactive:
            dprint(f'  - {card.card_text}')

        card.pile.remove(card)
        self.drills.add(card)
        card.set_pile(self.drills)

        # Discard any newly invalidated restricted drills
        for player in [self, self.opponent]:
            for drill_card in player.drills:
                if (drill_card is not card
                    and drill_card.restricted
                    and drill_card.style == card.style):
                    dprint(f'{player}\'s restricted {drill_card.name} invalidated')
                    player.discard(drill_card)

        for card_power in card.card_powers:
            self.register_card_power(card_power)

    def play_dragon_ball(self, card):
        dprint(f'{self} plays {card}')
        if not self.interactive:
            dprint(f'  - {card.card_text}')

        card.pile.remove(card)
        self.dragon_balls.add(card)
        card.set_pile(self.dragon_balls)

        self.check_for_dragon_ball_victory()

        # Dragon balls are executed immediately
        for card_power in card.card_powers:
            if isinstance(card_power, CardPowerDragonBall):
                card_power.on_play(self, State.PHASE)

    def play_non_combat_card(self, card):
        if isinstance(card, NonCombatCard):
            dprint(f'{self} plays {card}')
            if not self.interactive:
                dprint(f'  - {card.card_text}')
            card.pile.remove(card)
            self.non_combat.add(card)
            card.set_pile(self.non_combat)
            for card_power in card.card_powers:
                self.register_card_power(card_power)
        elif isinstance(card, PersonalityCard):
            self.play_ally(card)
        elif isinstance(card, DrillCard):
            self.play_drill(card)
        elif isinstance(card, DragonBallCard):
            self.play_dragon_ball(card)
        else:
            assert False

        return card
