import copy
import sys

from character import Character


class Cost:
    def __init__(self, power=None, life=None,
                 own_ally=None,
                 character_in_control_req=None,
                 ally_in_play_req=None):
        # Costs:
        self.power = power or 0
        self.life = life or 0
        # TODO: not sure if this should be int/list/Character/Card...
        self.own_ally = own_ally or 0

        # Requirements:
        self.character_in_control_req = character_in_control_req or []  # OR of list [Character,]
        if isinstance(self.character_in_control_req, Character):
            self.character_in_control_req = [self.character_in_control_req]

        self.ally_in_play_req = ally_in_play_req or []  # OR of list [Character,]
        if isinstance(self.ally_in_play_req, Character):
            self.ally_in_play_req = [self.ally_in_play_req]

    def copy(self):
        return copy.copy(self)

    def can_afford(self, player):
        if (self.character_in_control_req
            and player.control_personality.character not in self.character_in_control_req):
            return False

        if self.ally_in_play_req:
            allies_in_play = [x.character for x in player.allies + player.opponent.allies]
            if not any(x in allies_in_play for x in self.ally_in_play_req):
                return False

        return (player.control_personality.power_stage >= self.power
                and len(player.life_deck) >= self.life
                and len(player.allies) >= self.own_ally)

    def pay(self, player):
        assert self.can_afford(player)
        player.control_personality.reduce_power_stage(self.power)
        player.apply_life_damage(self.life)
        for _ in range(self.own_ally):
            ally = player.choose_personality(
                skip_main=True, prompt='Select an ally to sacrifice')
            # TODO: assuming remove from game for now
            player.remove_from_game(ally)

    @classmethod
    def none(cls):
        return Cost()

    @classmethod
    def energy_attack(cls, power=None, life=None):
        if power is not None or life is not None:
            power = power or 0
            life = life or 0
        else:
            power = 2
            life = 0
        return cls(power=power, life=life)
