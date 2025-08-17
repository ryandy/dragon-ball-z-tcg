import enum
import random
import sys

import numpy.random as np_random

from dbz.card_power import CardPower, CardPowerPass
from dbz.card_power_attack import CardPowerAttack
from dbz.state import State


class AIStrategy(enum.Enum):
    SURVIVAL = 1
    PERSONALITY = 2
    DRAGON_BALLS = 3


class AI:
    @staticmethod
    def choose(player, names, descriptions, allow_pass=True,
               refs=None, context=None, eval_maximize=True, immediate=True):
        # Check if there's only one option
        if allow_pass and not names:
            return None
        if not allow_pass and len(names) == 1:
            return 0

        if refs and isinstance(refs[0], CardPower):
            if allow_pass:
                refs.append(CardPowerPass())
            win_con_scores = [AI.get_card_power_eval(player, x, immediate=immediate) for x in refs]
            idx = random.randrange(len(refs))

            #idx = np_random.choice(range(len(refs)), size=1, p=[10**x for x in win_con_scores])
            #print(refs)
            #print(win_con_scores)
            #print([10**x for x in win_con_scores])
            #print(idx)
            #print(AI.get_current_game_score(player))
            #for score in win_con_scores:
            #    print(AI.get_choice_situational_score(player, score))

            scores = [AI.get_choice_situational_score(player, x) for x in win_con_scores]
            #print(scores)
            #print([10**x for x in scores])
            #idx = np_random.choice(range(len(refs)), size=1, p=[10**x for x in scores])
            weights=[10**x for x in scores]
            idx = random.choices(
                population=range(len(refs)), k=1, weights=weights)[0]
            #print(refs)
            #print(win_con_scores)
            #print(scores)
            #print(weights)
            #print(idx)
            #if weights and max(weights) > 3 and idx != len(refs) - 1:
            #    sys.exit(0)
            #for i in range(len(scores)):
            #    print(refs[i].name, scores[i], 10**scores[i])
            #print(f'choice: {idx}')
            #print(idx)
            #sys.exit(9)


            # TODO: Need to give default values for defensive powers below


            if idx == len(names):  # pass
                return None
            return idx

        if allow_pass and random.random() < 0.1:
            # Pass small % of the time
            return None
        if len(names) > 1 and names[-1] == 'Final Physical Attack' and random.random() < 0.95:
            # Almost never want to choose FPA if another choice exists
            return random.randrange(len(names) - 1)
        if len(names) == 1 and names[-1] == 'Final Physical Attack' and random.random() < 0.67:
            # Even when it's the only choice, probably want to pass instead of FPA sometimes
            return None
        # Random choice
        return random.randrange(len(names))

    @staticmethod
    def hasattr(card_power, attr):
        return hasattr(card_power, attr) and getattr(card_power, attr)

    @staticmethod
    def get_current_game_score(player, recurse=True):
        survival_turns_remaining = len(player.opponent.life_deck) / 5
        mpp_turns_remaining = ((15 - 5*(player.main_personality.level - 1) - player.anger) / 1.5
                                   if player.can_win_by_mpp() else 100)
        db_turns_remaining = max(0.5, (7 - len(player.dragon_balls)) / 0.5)

        if player.interactive:
            # TODO: infer deck's strategy
            pass
        else:
            if player.strategy == AIStrategy.SURVIVAL:
                survival_turns_remaining /= 2
                mpp_turns_remaining *= 2
            elif player.strategy == AIStrategy.PERSONALITY:
                mpp_turns_remaining /= 2
                db_turns_remaining *= 2
            elif player.strategy == AIStrategy.DRAGON_BALLS:
                db_turns_remaining /= 2
                mpp_turns_remaining *= 2

        turns_remaining = (survival_turns_remaining, mpp_turns_remaining, db_turns_remaining)

        if not recurse:
            return turns_remaining

        opp_turns_remaining = AI.get_current_game_score(player.opponent, recurse=False)

        min_turns_remaining = min(turns_remaining + opp_turns_remaining)
        return ((max(2 - 0.5 * (turns_remaining[0] / min_turns_remaining), 0.5),
                 max(2 - 0.5 * (opp_turns_remaining[0] / min_turns_remaining), 0.5)),
                (max(2 - 0.5 * (turns_remaining[1] / min_turns_remaining), 0.5),
                 max(2 - 0.5 * (opp_turns_remaining[1] / min_turns_remaining), 0.5)),
                (max(2 - 0.5 * (turns_remaining[2] / min_turns_remaining), 0.5),
                 max(2 - 0.5 * (opp_turns_remaining[2] / min_turns_remaining), 0.5)))

    @staticmethod
    def get_choice_situational_score(player, win_con_scores):
        game_score = AI.get_current_game_score(player)
        scores = []
        for win_con in range(3):        
            for off_def in range(2):
                scores.append(win_con_scores[win_con][off_def] * game_score[win_con][off_def])
        scores.sort(reverse=True)
        return 0.8*scores[0] + 0.2*scores[1]

    @staticmethod
    def get_card_power_eval(player, card_power, immediate=True):
        # Returns ((f, f), (f, f), (f, f))
        #   Survival Victory Off/Def, MPP Victory Off/Def, DB Victory Off/Def
        #   All values roughly in range [-3, 3]
        if AI.hasattr(card_power, 'get_ai_eval'):
            return card_power.get_ai_eval(player, immediate=immediate)

        description = card_power.description.lower()
        survive_off, survive_def = 0, 0
        mpp_off, mpp_def = 0, 0
        db_off, db_def = 0, 0

        if AI.hasattr(card_power, 'own_anger'):
            anger_delta = card_power.own_anger
            if immediate:
                anger_delta = min(card_power.own_anger, 5 - player.anger)
            mpp_off += anger_delta

        if AI.hasattr(card_power, 'opp_anger'):
            anger_delta = -card_power.opp_anger
            if immediate:
                anger_delta = min(-card_power.opp_anger, player.opponent.anger)
            mpp_def += anger_delta

        if AI.hasattr(card_power, 'main_power'):
            # Good for survival, not super important for MPP or DB
            power_delta = card_power.main_power
            if immediate:
                power_delta = min(card_power.main_power, 10 - player.main_personality.power_stage)

            # power_delta: 0 1 2 3 4 5 6 7 8 9 10
            # value:                 1          2
            survive_off += power_delta / 5  # power -> afford energy attacks to do life damage
            survive_def += power_delta / 5  # power -> prevent life damage from physical attacks

        if AI.hasattr(card_power, 'opp_power'):
            # Good for survival, not super important for MPP or DB
            power_delta = -card_power.opp_power
            if immediate:
                power_delta = min(-card_power.opp_power, player.opponent.main_personality.power_stage)
            survive_off += power_delta / 5
            survive_def += power_delta / 5

        if AI.hasattr(card_power, 'any_power'):
            main_power_delta, ally_power_delta = card_power.any_power, card_power.any_power
            if immediate:
                main_power_delta = min(card_power.any_power, 10 - player.main_personality.power_stage)
                ally_power_delta = 0
                for ally in player.allies:
                    ally_power_delta = max(ally_power_delta,
                                           min(card_power.any_power, 10 - ally.power_stage))
            power_delta = max(main_power_delta, ally_power_delta)

            survive_off += power_delta / 5
            survive_def += power_delta / 5

            db_off += ally_power_delta / 10

        if AI.hasattr(card_power, 'force_end_combat'):
            mpp_off += 1
            db_off += 1.5
            if not immediate or len(player.hand) + 2 <= len(player.opponent.hand):
                survive_def += 0.5
                mpp_def += 0.5
                db_def += 0.5

        if AI.hasattr(card_power, 'rejuvenate_count'):
            rejuvenate_count = card_power.rejuvenate_count
            if immediate:
                # TODO: look at exact cards we would recycle and get their (discounted?) hints
                rejuvenate_count = min(rejuvenate_count, len(player.discard_pile))
            survive_off += rejuvenate_count / 3
            survive_def += rejuvenate_count / 2
            db_off += rejuvenate_count / 2

        if AI.hasattr(card_power, 'rejuvenate_bottom_count'):
            rejuvenate_count = card_power.rejuvenate_bottom_count
            if immediate:
                # TODO: look at exact cards we would recycle and get their (discounted?) hints
                rejuvenate_count = min(rejuvenate_count, len(player.discard_pile))
            survive_off += rejuvenate_count / 3
            survive_def += rejuvenate_count / 2
            db_off += rejuvenate_count / 2

        if AI.hasattr(card_power, 'rejuvenate_choice_count'):
            rejuvenate_count = card_power.rejuvenate_choice_count
            if immediate:
                # TODO: look at exact cards we could recycle and get their (discounted?) hints
                rejuvenate_count = min(rejuvenate_count, len(player.discard_pile))
            survive_off += rejuvenate_count / 3
            survive_def += rejuvenate_count / 2
            db_off += rejuvenate_count / 2

        if isinstance(card_power, CardPowerAttack):
            if immediate:
                # TODO: estimate how much power damage would convert to life damage
                attacker = card_power.player or player
                damage = card_power.damage.resolve(attacker)
                life_damage = damage.life
                power_damage = damage.power
            else:
                life_damage = damage.life + sum(x.life_add for x in damage.mods)
                power_damage = 1 if damage.use_pat else 0
                power_damage *= max([1, damage.power_mult] + [x.power_mult for x in damage.mods])
                power_damage += damage.power + sum(x.power_add for x in damage.mods)

            survive_off += life_damage / 2  # If you're trying to mill opp, this is how you do it
            survive_def += life_damage / 8  # Milling a miller's deck might not do much
            mpp_def += life_damage / 2  # Best counter to MPP is to burn their deck
            db_def += life_damage / 4  # Good counter to DB but their deck becomes more DB-dense

            survive_off += power_damage / 4  # Once opp power is depleted, power attacks will mill
            survive_def += power_damage / 4  # Opp needs power to do energy attacks
            db_def += power_damage / 8  # They need power to do DB-stealing energy attacks

            if (player.can_steal_dragon_ball()
                and life_damage > 0
                and len(player.allies) > 0
                and player.main_personality.power_stage < 2):
                db_off += 2
                db_def += 2

            if (player.can_steal_dragon_ball()
                and life_damage >= 5):
                db_off += 2
                db_def += 2

        if 'dragon ball' in description:
            # TODO: needs improvement
            #   if card allows for stealing, check to see if we even can steal
            #   infer db_def effect?
            #   immediate vs later
            if (('steal' in description or 'capture' in description)
                and not player.can_steal_dragon_ball()):
                pass
            else:
                db_off += 2

        if not card_power.cost.is_none():
            # power:    1   2     3    4
            # factor:  0.9 0.75  0.6  0.5
            power_cost = card_power.cost.power
            # TODO: subtract instead of multiply?
            #       what if one of the scores is already negative?
            #       if it's bad _and_ we have to pay, it needs to become worse
            survive_off *= (1 - power_cost / 8)
            survive_def *= (1 - power_cost / 8)
            mpp_off *= (1 - power_cost / 8)
            mpp_def *= (1 - power_cost / 8)
            db_off *= (1 - power_cost / 8)
            db_def *= (1 - power_cost / 8)

            other_cost = card_power.cost.discard + card_power.cost.own_ally
            if other_cost:
                survive_off *= 0.5
                survive_def *= 0.5
                mpp_off *= 0.5
                mpp_def *= 0.5
                db_off *= 0.5
                db_def *= 0.5

        if card_power.is_floating:
            if survive_off:
                survive_off += 0.5
            if survive_def:
                survive_def += 0.5
            if mpp_off:
                mpp_off += 0.5
            if mpp_def:
                mpp_def += 0.5
            if db_off:
                db_off += 0.5
            if db_def:
                db_def += 0.5

        if card_power.name == 'Pass':
            survive_off += 0.25
            survive_def += 0.25
            mpp_off += 0.25
            mpp_def += 0.25
            db_off += 0.25
            db_def += 0.25
            if State.PASS_COUNT > 0:
                db_off += 1.5  # Better than forcing end of combat

        if card_power.name == 'Final Physical Attack':
            if State.PASS_COUNT == 0:
                survive_off *= 0.5
                survive_def *= 0.5
                mpp_off *= 0.5
                mpp_def *= 0.5
                db_off *= 0.5
                db_def *= 0.5

        return ((survive_off, survive_def),
                (mpp_off, mpp_def),
                (db_off, db_def))
