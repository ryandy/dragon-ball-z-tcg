import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Chiaotzu\'s Physical Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '250'
RARITY = 6
DECK_LIMIT = None
CHARACTER = 'Chiaotzu'
STYLE = None
CARD_TEXT = ('Stops all heroes from losing 1 life card of damage from every attack for the'
             ' remainder of Combat. Remove from the game after use.')


class CardPowerCPD(CardPowerNonCombatAttack):
    def on_success(self, player, phase):
        class CardPowerCPD_DamageModification(CardPowerOnDamageModification):
            def _on_damage_modification(_self, _attacker, _phase):
                if _attacker.opponent.personality.is_hero:
                    return DamageModifier(life_add=-1)
            def on_physical_damage_modification(_self, _attacker, _phase):
                return _self._on_damage_modification(_attacker, _phase)
            def on_energy_damage_modification(_self, _attacker, _phase):
                return _self._on_damage_modification(_attacker, _phase)
        card_power = CardPowerCPD_DamageModification(self.name, self.description)
        card_power.exhaust_after_this_turn()
        card_power.set_floating()
        player.register_card_power(card_power)


CARD_POWER = CardPowerCPD(NAME, CARD_TEXT, remove_from_game=True)
