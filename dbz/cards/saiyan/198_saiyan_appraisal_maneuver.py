import pathlib
import sys

from card_factory import CardFactory
from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier
from drill_card import DrillCard
from non_combat_card import NonCombatCard


TYPE = 'Non-Combat'
NAME = 'Saiyan Appraisal Maneuver'
SAGA = 'Saiyan'
CARD_NUMBER = '198'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Saiyan'
CARD_TEXT = ('Name a Non-Combat card and foes with any in their deck must remove them'
             ' from the game. Remove from the game after use.')


class CardPowerNonCombatAttackSAM(CardPowerNonCombatAttack):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        
        cards = []
        root_card_path = pathlib.Path(f'./cards')
        card_paths = list(sorted(root_card_path.glob(f'**/*.py')))
        for card_path in card_paths:
            card = CardFactory.from_file(card_path)
            if card.deck_limit == 0:
                continue
            if isinstance(card, NonCombatCard) or isinstance(card, DrillCard):
                cards.append(card)

        cards.sort(key=lambda x: x.name.lower())
        idx = self.player.choose([str(c) for c in cards],
                                 [c.card_text for c in cards],
                                 allow_pass=False,
                                 prompt='Select a card to completely remove from opponent\'s deck')
        card = cards[idx]
        for idx in reversed(range(len(self.player.opponent.life_deck))):
            if self.player.opponent.life_deck.cards[idx].get_id() == card.get_id():
                self.player.opponent.remove_from_game(self.player.opponent.life_deck.cards[idx])


CARD_POWER = CardPowerNonCombatAttackSAM(NAME, CARD_TEXT, remove_from_game=True)
