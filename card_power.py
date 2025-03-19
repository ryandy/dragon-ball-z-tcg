import abc
import sys

from state import State


class CardPower(abc.ABC):
    def __init__(self, name, description, cost,
                 heroes_only=False, villains_only=False, saiyan_only=False, namekian_only=False,
                 card=None, is_floating=False):
        self.name = name
        self.description = description
        self.cost = cost
        self.heroes_only = heroes_only
        self.villains_only = villains_only
        self.saiyan_only = saiyan_only
        self.namekian_only = namekian_only
        self.card = card
        self.is_floating = is_floating
        self.valid_from = None  # tuple of (turn #, combat round #)
        self.valid_until = None  # tuple of (turn #, combat round #)

    def __repr__(self):
        suffix = ' (*)' if self.is_floating else ''
        return f'{self.name}{suffix}'

    def register_card(self, card):
        self.card = card

    def set_floating(self):
        self.is_floating = True

    def exhaust_until_next_turn(self):
        self.valid_from = (State.TURN + 1, 0)

    def exhaust_after_next_combat_phase(self):
        self.valid_until = (State.TURN, State.COMBAT_ROUND + 1)

    def exhaust_after_this_turn(self):
        self.valid_until = (State.TURN + 1, -1)

    def is_exhausted(self):
        cur_time = State.get_time()
        valid = ((not self.valid_from or self.valid_from <= cur_time)
                 and (not self.valid_until or cur_time <= self.valid_until))
        return not valid

    def is_personality_restricted(self, personality):
        '''If this card power cannot be activated by a given personality'''
        if self.heroes_only:
            return not personality.is_hero
        if self.villains_only:
            return personality.is_hero
        if self.saiyan_only:
            return not personality.character.has_saiyan_heritage()
        if self.namekian_only:
            return not personality.character.has_namekian_heritage()
        return False
