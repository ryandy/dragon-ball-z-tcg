import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier
from dragon_ball_card import DragonBallCard


TYPE = 'Non-Combat'
NAME = 'Goku\'s Lucky Break'
SAGA = 'Saiyan'
CARD_NUMBER = '202'
RARITY = 5
DECK_LIMIT = None
CHARACTER = 'Goku'
STYLE = None
CARD_TEXT = ('Search your Life Deck for a Dragon Ball and place it into play. Remove from the game'
             ' after use.')


class CardPowerNonCombatAttackGLB(CardPowerNonCombatAttack):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)

        cards, names, descriptions = [], [], []
        for card in player.life_deck:
            if (isinstance(card, DragonBallCard)
                and card.can_be_played(player)):
                cards.append(card)
                names.append(card.name)
                descriptions.append(card.card_text)
        if cards:
            idx = player.choose(names, descriptions, allow_pass=False,
                                prompt='Select a Dragon Ball to play from your Life Deck')
            card = cards[idx]
            player.play_dragon_ball(card)

        # Regardless of outcome, shuffle the deck after "searching" it
        player.life_deck.shuffle()


CARD_POWER = CardPowerNonCombatAttackGLB(NAME, CARD_TEXT, remove_from_game=True)
