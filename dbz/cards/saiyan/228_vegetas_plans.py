import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier
from dbz.dragon_ball_card import DragonBallCard


TYPE = 'Non-Combat'
NAME = 'Vegeta\'s Plans'
SAGA = 'Saiyan'
CARD_NUMBER = '228'
RARITY = 5
DECK_LIMIT = 1
CHARACTER = 'Vegeta'
STYLE = None
CARD_TEXT = ('Select any Dragon Ball in your deck and put it into play.'
             ' Remove from the game after use.')


class CardPowerNonCombatAttackVP(CardPowerNonCombatAttack):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)

        # Try to only collect playable DBs, but fall back to all DBs
        cards = [x for x in player.life_deck
                 if isinstance(x, DragonBallCard) and x.can_be_played(player)]
        if not cards:
            cards = [x for x in player.life_deck if isinstance(x, DragonBallCard)]

        if cards:
            idx = player.choose([x.name for x in cards],
                                [x.card_text for x in cards],
                                allow_pass=False,
                                prompt='Select a Dragon Ball to play from your deck')
            db = cards[idx]

            # Shuffle deck before playing DB card, as it may affect the deck e.g. DB7
            player.shuffle_deck()

            if db.can_be_played(player):
                player.play_dragon_ball(db)
            else:
                player.discard(db)
        else:
            # Regardless of outcome, shuffle the deck after "searching" it
            player.shuffle_deck()


CARD_POWER = CardPowerNonCombatAttackVP(NAME, CARD_TEXT, remove_from_game=True)
