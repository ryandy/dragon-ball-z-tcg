import sys

from dbz.card_power_defense import CardPowerAnyDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier
from dbz.personality_card import PersonalityCard


TYPE = 'Combat'
NAME = 'Unexpected Allies'
SUBTYPE = 'Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '218'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Search your Life Deck or discard pile for an Ally and put them into play at'
             ' their highest power stage.')


class CardPowerAnyDefenseUA(CardPowerAnyDefense):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)

        cards, names, descriptions = [], [], []
        for card in (player.life_deck + player.discard_pile):
            if (isinstance(card, PersonalityCard)
                and card.can_be_played(player)):
                cards.append(card)
                names.append(f'{card.name} ({card.pile.name})')
                descriptions.append(card.card_text)
        if cards:
            idx = player.choose(names, descriptions, allow_pass=False,
                                prompt='Select an Ally to play')
            ally = cards[idx]
            player.play_ally(ally)
            ally.set_power_stage_max()

        # Regardless of outcome, shuffle the deck after "searching" it
        player.shuffle_deck()


CARD_POWER = CardPowerAnyDefenseUA(NAME, CARD_TEXT, damage_modifier=DamageModifier.none())
