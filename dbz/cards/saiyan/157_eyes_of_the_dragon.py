import sys

from card_power_attack import CardPowerNonCombatAttack
from card_power_on_attack_resolved import CardPowerOnAttackResolved
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier
from dragon_ball_card import DragonBallCard


TYPE = 'Non-Combat'
NAME = 'Eyes of the Dragon'
SAGA = 'Saiyan'
CARD_NUMBER = '157'
RARITY = 3
DECK_LIMIT = 1
CHARACTER = None
STYLE = None
CARD_TEXT = ('After you perform a successful energy attack, search your Life Deck for a'
             ' Dragon Ball then place it in play and capture a Dragon Ball from your opponent.')


class CardPowerOnAttackResolvedEOTD(CardPowerOnAttackResolved):
    def on_condition(self, phase, damage, is_physical):
        return (self.player is phase.player  # attacking
                and not damage.was_stopped()  # successful
                and not is_physical)  # energy

    def on_effect(self, phase, damage, is_physical):
        # Play DB from Life Deck
        cards, names, descriptions = [], [], []
        for card in self.player.life_deck:
            if (isinstance(card, DragonBallCard)
                and card.can_be_played(self.player)):
                cards.append(card)
                names.append(card.name)
                descriptions.append(card.card_text)
        if cards:
            idx = self.player.choose(names, descriptions, allow_pass=False,
                                     prompt='Select a Dragon Ball to play from your Life Deck')
            card = cards[idx]
            self.player.play_dragon_ball(card)

        # Steal DB from opponent
        self.player.steal_dragon_ball()


CARD_POWER = CardPowerOnAttackResolvedEOTD(NAME, CARD_TEXT, choice=True)
