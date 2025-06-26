import abc
import copy
import sys

from dbz.cost import Cost
from dbz.state import State


class CardPower(abc.ABC):
    def __init__(self, name, description, cost,
                 exhaust=True, exhaust_until_next_turn=False,
                 discard=True, remove_from_game=False,
                 heroes_only=False, villains_only=False, saiyan_only=False, namekian_only=False,
                 card=None, is_floating=False):
        self.name = name
        self.description = description
        self.cost = cost.copy()
        self.exhaust_after_use = exhaust
        self.exhaust_until_next_turn_after_use = exhaust_until_next_turn
        self.discard_after_use = discard
        self.remove_from_game_after_use = remove_from_game
        self.heroes_only = heroes_only
        self.villains_only = villains_only
        self.saiyan_only = saiyan_only
        self.namekian_only = namekian_only
        self.card = card
        self.is_floating = is_floating
        self.valid_from = None  # tuple of (turn #, combat round #)
        self.valid_until = None  # tuple of (turn #, combat round #)
        self.deactivated = False  # Can be temporarily turned on/off without exhausting
        self.player = None
        self.resolved_count = 0

    def __repr__(self):
        suffix = ' (*)' if self.is_floating else ''
        return f'{self.name}{suffix}'

    def copy(self):
        # Note: do not deep copy self.card
        card_power_copy = copy.copy(self)
        card_power_copy.cost = self.cost.copy()
        return card_power_copy

    def register_card(self, card):
        '''Source card is registered with the card power after the card is instantiated'''
        self.card = card

    def register_player(self, player):
        '''Owning player is registered with the card power when it is registered with the player'''
        self.player = player

    def activate(self):
        self.deactivated = False

    def deactivate(self):
        self.deactivated = True

    def is_deactivated(self):
        return self.deactivated

    def set_floating(self):
        self.is_floating = True
        self.card = None

    def exhaust_until_next_turn(self):
        self.valid_from = (State.TURN + 1, 0)

    def exhaust_after_this_combat_attack_phase(self):
        # Valid during current combat attack phase only
        self.valid_until = (State.TURN, State.COMBAT_ROUND + 1)

    def exhaust_after_next_combat_attack_phase(self):
        # Valid during phases +1 and +2 (one more of each: attack and defense)
        self.valid_until = (State.TURN, State.COMBAT_ROUND + 3)

    def exhaust_after_this_turn(self):
        self.valid_until = (State.TURN + 1, 0)

    def exhaust_after_turns(self, count):
        self.valid_until = (State.TURN + 1 + count, 0)

    def is_exhausted(self):
        cur_time = State.get_time()
        valid = ((not self.valid_from or self.valid_from <= cur_time)
                 and (not self.valid_until or cur_time < self.valid_until))
        return not valid

    def is_restricted(self, player):
        '''If this card power cannot be activated by a given personality'''
        if self.heroes_only:
            return not player.control_personality.is_hero
        if self.villains_only:
            return player.control_personality.is_hero
        if self.saiyan_only:
            return not player.control_personality.character.has_saiyan_heritage()
        if self.namekian_only:
            return not player.control_personality.character.has_namekian_heritage()
        return False

    def on_pay_cost(self, player, phase):
        player.pay_cost(self)

    def on_resolved(self):
        if self.card:
            self._on_resolved_with_card()
        else:
            self._on_resolved_without_card()

    def _on_resolved_with_card(self):
        if self.exhaust_until_next_turn_after_use:
            self.player.exhaust_card_until_next_turn(self.card)
        elif self.exhaust_after_use:
            self.player.exhaust_card(self.card)

        card_in_pile = (self.card.attached_to is None)
        if self.remove_from_game_after_use:
            self.player.remove_from_game(self.card, exhaust_card=False, card_in_pile=card_in_pile)
        elif self.discard_after_use:
            self.player.discard(self.card, exhaust_card=False, card_in_pile=card_in_pile)

    def _on_resolved_without_card(self):
        if self.exhaust_until_next_turn_after_use:
            self.exhaust_until_next_turn()
        elif self.exhaust_after_use:
            self.player.exhaust_card_power(self)


class CardPowerPass(CardPower):
    def __init__(self):
        super().__init__('Pass', 'Do Nothing.', cost=Cost.none())
