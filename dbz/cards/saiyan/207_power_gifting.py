import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Power Gifting'
SAGA = 'Saiyan'
CARD_NUMBER = '207'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('One ally gives your Main Personality power on a stage for stage basis, reducing their'
             ' total and boosting your Main Personality\'s. Remove from the game after use.')


class CardPowerNonCombatAttackPG(CardPowerNonCombatAttack):
    def is_restricted(self, player):
        if len(player.allies) == 0:
            return True
        return super().is_restricted(player)

    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)

        ally = player.choose_personality(
            skip_main=True, prompt='Select an ally to take power from')

        max_power_gift = min(ally.power_stage, 10 - player.main_personality.power_stage)
        assert 0 <= max_power_gift <= 10

        idx = player.choose([f'{x} power stage{"s" if x > 1 else ""}'
                             for x in range(1, max_power_gift + 1)], [],
                            prompt='Select number of power stages to gift')
        power = 0 if idx is None else idx+1

        ally.adjust_power_stage(-power)
        player.main_personality.adjust_power_stage(power)


CARD_POWER = CardPowerNonCombatAttackPG(NAME, CARD_TEXT, remove_from_game=True)
