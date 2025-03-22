import abc
import sys

from character import Character
from rarity import Rarity
from saga import Saga
from style import Style


class Card(abc.ABC):
    def __init__(self, name, saga, card_number, rarity, deck_limit, character, style,
                 card_text, card_power):
        self.name = name
        if isinstance(saga, str):
            saga = Saga[saga.upper()]
        self.saga = Saga(saga)
        self.card_number = card_number
        self.rarity = Rarity(rarity)
        self.deck_limit = deck_limit

        if isinstance(character, str):
            character = Character[character.replace('-', '_').upper()]
        self.character = Character(character) if character else None

        if isinstance(style, str):
            style = Style[style.upper()]
        self.style = Style(style) if style else Style.FREESTYLE

        self.card_text = card_text
        if isinstance(card_power, list):
            self.card_powers = card_power
        else:
            self.card_powers = [card_power]

        self.pile = None  # Current pile

    def __repr__(self):
        return f'{self.name}'

    def __copy__(self):
        '''Cards cannot be copied'''
        assert False

    def __deepcopy__(self):
        '''Cards cannot be copied'''
        assert False

    def set_pile(self, pile):
        assert self.pile is not pile
        self.pile = pile

    def get_id(self):
        return f'{self.saga.name.lower()}.{self.card_number}'
