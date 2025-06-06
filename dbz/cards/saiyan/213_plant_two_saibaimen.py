import sys

from card_power_on_end_of_power_up_phase import CardPowerOnEndOfPowerUpPhase
from card_power_on_entering_turn import CardPowerOnEnteringTurn
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier
from personality_card import PersonalityCard
from state import State


TYPE = 'Non-Combat'
NAME = 'Plant Two Saibaimen'
SAGA = 'Saiyan'
CARD_NUMBER = '213'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Use this card at the end of your Power Up step. Skip Combat this turn.'
             ' At the beginning of your next turn, search your Life Deck and/or discard pile'
             ' for your highest level Saibaimen card and place it into play.'
             ' Remove from the game after use.')


class CardPowerOnEnteringTurnPTS(CardPowerOnEnteringTurn):
    def on_condition(self):
        return State.TURN_PLAYER is self.player  # own turn

    def on_effect(self):
        cards = [x for x in self.player.life_deck
                 if isinstance(x, PersonalityCard) and x.character == Character.SAIBAIMEN]
        if cards:
            max_level = max(x.level for x in cards)
            cards = [x for x in cards if x.level == max_level and x.can_be_played(self.player)]
            if cards:
                idx = self.player.choose([x.name for x in cards],
                                         [x.card_text for x in cards],
                                         allow_pass=False,
                                         prompt='Select a Saibaimen to play from your deck')
                ally = cards[idx]
                self.player.play_ally(ally)

        # Regardless of outcome, shuffle the deck after "searching" it
        self.player.shuffle_deck()


class CardPowerOnEndOfPowerUpPhasePTS(CardPowerOnEndOfPowerUpPhase):
    def on_condition(self, phase):
        return phase.player is self.player  # own Power Up step

    def on_effect(self, phase):
        phase.set_force_skip_combat()

        description = ('At the beginning of your next turn, search your Life Deck and/or discard'
                       ' pile for your highest level Saibaimen card and place it into play.')
        card_power_next_turn = CardPowerOnEnteringTurnPTS(
            self.name, description, choice=False, exhaust=True, discard=False)
        card_power_next_turn.set_floating()
        self.player.register_card_power(card_power_next_turn)


CARD_POWER = CardPowerOnEndOfPowerUpPhasePTS(
    NAME, CARD_TEXT, choice=True, exhaust=True, remove_from_game=True)
