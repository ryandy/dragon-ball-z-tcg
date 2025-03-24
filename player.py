import collections
import random
import sys

from card_power import CardPower
from card_power_attack import CardPowerAttack
from card_power_defense import CardPowerDefense
from card_power_defense_shield import (CardPowerPhysicalDefenseShield,
                                       CardPowerEnergyDefenseShield,
                                       CardPowerAnyDefenseShield)
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
            card.register_owner(self)
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
        # TODO: Need to discard/remove covered allies when the overlaid one leaves play
        self.covered_allies = Pile('CoveredAllies')  # Temporary home for overlaid allies
        self.non_combat = Pile('Non-Combat')
        self.drills = Pile('Drills')
        self.dragon_balls = Pile('DragonBalls')

        self.personality = self.personality_cards[0]
        self.personality.init_power_stage_for_main()
        self.register_card_powers(self.personality.card_powers)
        self.interactive = (self.name() == 'Goku') if State.INTERACTIVE else False

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
        # TODO: Append differentiator if both players are using the same character
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
                and not card_power.is_personality_restricted(self.personality)
                and card_power.cost.can_afford(self)):
                filtered_card_powers.append(card_power)
        return filtered_card_powers

    def raise_level(self):
        next_level = self.personality.level + 1
        next_level_idx = next_level - 1

        # Check for win condition
        if (next_level_idx == len(self.personality_cards) - 1
            and len(self.personality_cards) >= len(self.opponent.personality_cards)):
            dprint(f'{self.name()} levels up to Lv{next_level}!')
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

    def check_for_dragon_ball_victory(self):
        set_counts = collections.defaultdict(int)
        for card in self.dragon_balls:
            set_counts[card.db_set] += 1
            if set_counts[card.db_set] == 7:
                raise GameOver(f'{self.name()} has collected all 7 {card.db_set} Dragon Balls',self)

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
            card.set_pile(None)  # Temporarily move card so it can move back when recycled
            self.recycle_dragon_ball(card)
            return None

        # Check if an unplayable drill was drawn - can shuffle back into deck
        if (dest_pile is self.hand
            and isinstance(card, DrillCard)
            and card.style != Style.FREESTYLE
            and any(x.style != card.style for x in self.drills if x.style != Style.FREESTYLE)):
            if self.interactive:
                dprint(f'{self.name()} draws unplayable {card.name}')
            idx = self.choose(['Shuffle it back into deck.', 'Keep it.'],
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

    def discard(self, card, remove_from_game=False, exhaust_card=True, card_in_pile=True):
        '''Hand/Table -> Discard/Removed'''
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
            dprint(f'{self.name()} removes {card} from game')
            self.removed_pile.add(card)
            card.set_pile(self.removed_pile)
        else:  # discard
            dprint(f'{self.name()} discards {card}')
            self.discard_pile.add(card)
            card.set_pile(self.discard_pile)

    def recycle_dragon_ball(self, card):
        '''Card has already been removed from its source pile, so currently in no-mans-land'''
        dup_restricted = any(card.is_duplicate(x)
                             for x in self.dragon_balls + self.opponent.dragon_balls)
        if dup_restricted:
            # If this is a duplicate of a dragon ball in play, remove it from the game
            self.discard(card, remove_from_game=True, card_in_pile=False)
        else:
            dprint(f'{self.name()} recycles {card}')
            self.life_deck.add_bottom(card)
            card.set_pile(self.life_deck)

    def steal_dragon_ball(self):
        card = self.choose_opponent_dragon_ball()
        if not card:
            return

        dprint(f'{self.name()} steals {card.name}!')
        self.opponent.dragon_balls.remove(card)
        self.dragon_balls.add(card)
        card.set_pile(self.dragon_balls)

        for idx in reversed(range(len(self.opponent.card_powers))):
            if self.opponent.card_powers[idx].card is card:
                card_power = self.opponent.card_powers[idx]
                dprint(f'{self.name()} takes over {card_power} card power')
                del self.opponent.card_powers[idx]
                self.register_card_power(card_power)

    def rejuvenate(self):
        card = self.discard_pile.remove_top()
        if card:
            dprint(f'{self.name()} rejuvenates with {card}')
            self.life_deck.add_bottom(card)
            card.set_pile(self.life_deck)
        else:
            dprint(f'{self.name()} failed to rejuvenate because the discard pile is empty')

    def _apply_damage(self, damage, src_personality=None, is_physical=None):
        damage = damage.resolve(self.opponent)
        dprint(f'{self.name()} takes {damage}')

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
        power_damage = max(0, power_damage)
        target_personality = self.personality
        if power_damage:
            target_personality = self.choose_damage_target()
            if target_personality is not self.personality:
                dprint(f'{self.name()} selects {target_personality.name} to take damage')

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
            dprint(f'{self.opponent.name()} can steal a dragon ball instead of'
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
                dprint(f'{self.name()} takes 1 life damage: {card_discarded}')

        # Check for Dragon Ball Life Card Capture
        if discard_count >= 5 and src_personality:
            self.opponent.steal_dragon_ball()

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
        dprint(f'{level : <5} {name : <9} {power : >5}pwr {life : >2}hp {discard : >2}dp'
               f' {allies : >2}al {dbs : >2}db {drills : >2}dr {non_combat : >2}nc {hand : >2}hd')
        for ally in self.allies:
            level = f'Lv{ally.level}'
            name = ally.character.name.title()
            power = ally.power_stage
            pat_idx = ally.get_physical_attack_table_index()
            power = f'{power}({pat_idx})'
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
                suffix = f' ({card.owner.name()}\'s){suffix}'

            names.append(f'{card.name}{suffix}')
            descriptions.append(card.card_text)

        idx = self.choose(names, descriptions, allow_pass=False, prompt=prompt)
        return self.opponent.dragon_balls.cards[idx]

    def choose_damage_target(self):
        if len(self.allies) == 0:
            return self.personality

        names, descriptions = [], []
        for  personality in ([self.personality] + self.allies.cards):
            names.append(f'{personality.name} ({personality.power_stage}/10)')
            descriptions.append(personality.card_text)

        idx = self.choose(names, descriptions, allow_pass=False,
                          prompt='Select a personality to take power stages of damage')
        if idx == 0:
            return self.personality
        return self.allies.cards[idx-1]

    def choose_hand_non_combat_card(self):
        filtered = []
        for card in self.hand:
            if (isinstance(card, NonCombatCard)
                or (isinstance(card, DrillCard) and card.style == Style.FREESTYLE)):
                filtered.append(card)
            elif isinstance(card, DragonBallCard):
                # Only 1 of each Dragon Ball set/number can be on the table at a time
                dup_restricted = any(card.is_duplicate(x)
                                     for x in self.dragon_balls + self.opponent.dragon_balls)
                if not dup_restricted:
                    filtered.append(card)
            elif isinstance(card, PersonalityCard):
                is_overlay = any(
                    (x.character == card.character and x.level == card.level - 1)
                    for x in self.allies)

                # Cannot be the same character/level as any ally in play
                # TODO: Saibaimen exception
                dup_restricted = any(x.get_name_level() == card.get_name_level()
                                     for x in self.allies + self.opponent.allies)
                # Cannot be a different hero/villain status than Main Personality
                hero_restricted = card.is_hero != self.personality.is_hero
                # Cannot be the same character as either Main Personality
                mp_restricted = card.character in [self.personality.character,
                                                   self.opponent.personality.character]

                # Cannot be a higher level than Main Personality unless overlaying
                level_restricted = not is_overlay and (card.level > self.personality.level)

                # Cannot be the same character as an ally you have in play unless overlaying
                # TODO: Saibaimen exception
                char_restricted = not is_overlay and any(
                    x.character == card.character for x in self.allies)
                if (not dup_restricted
                    and not hero_restricted
                    and not mp_restricted
                    and not level_restricted
                    and not char_restricted):
                    filtered.append(card)
            elif isinstance(card, DrillCard):
                # Styled drills cannot be played if they are duplicates of a drill you have in
                # play, are a different style than a drill you have in play, or are restricted and
                # are the same style as any styled drill in play.
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
        elif isinstance(card, PersonalityCard):
            # TODO: Saibaimen can choose whether/which to overlay
            covered_ally = None
            for ally in self.allies:
                if ally.character == card.character and ally.level == card.level - 1:
                    covered_ally = ally
                    break

            card.init_power_stage_for_ally()
            if covered_ally:
                card.set_power_stage_max()
                self.exhaust_card(covered_ally)
                self.allies.remove(covered_ally)
                self.covered_allies.add(covered_ally)

            self.allies.add(card)
            card.set_pile(self.allies)

            for card_power in card.card_powers:
                self.register_card_power(card_power)
            self.deactivate_card_powers(card)  # Card powers deactivated until they take over combat
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
            self.check_for_dragon_ball_victory()
        else:
            assert False

        return card
