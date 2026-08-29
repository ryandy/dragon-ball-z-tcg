import enum
import random
import sys

from collections import defaultdict


'''
Booster rates from: magic.wizards.com/en/news/feature/collecting-edge-of-eternities


Common Total: 81
Common Colorless: 5
Common Gold (command bridge): 1
Common Each Color: ~15

Uncommon Total:      100
Uncommon Colorless:    5
Uncommon Gold:        10
Uncommon Each Color: ~17

Rare Total: 60
Rare Colorless (inc. secluded starforge): 5
Rare Gold (inc. shock lands): 16
Rare Each Color: ~8
'''

class Color(enum.Enum):
    WHITE = 0
    BLUE = 1
    BLACK = 2
    RED = 3
    GREEN = 4
    GOLD = 5
    COLORLESS = 6
    ANY = 7


class Rarity(enum.Enum):
    COMMON = 0
    UNCOMMON = 1
    RARE = 2
    MYTHIC = 3


class MtgSet(enum.Enum):
    EOE = 0
    EOS = 1  # Stellar Sights lands
    SPG = 2  # Special Guests
    

class Card:
    def __init__(self, rarity, color=None, mtg_set=None):
        self.rarity = rarity
        self.color = color
        self.mtg_set = mtg_set
        
        if self.color is None:
            if rarity == Rarity.COMMON:
                self.color = get_random_color_common2()
            elif rarity == Rarity.UNCOMMON:
                self.color = get_random_color_uncommon()
            elif rarity == Rarity.RARE:
                self.color = get_random_color_rare()
            else:
                self.color = get_random_color_mythic()

        if self.mtg_set is None:
            self.mtg_set = MtgSet.EOE


    def __repr__(self):
        return f'{self.color.name} {self.rarity.name} {self.mtg_set.name}'

    def __hash__(self):
        return 10 * 10 * self.color.value + 10 * self.rarity.value + self.mtg_set.value

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __lt__(self, other):
        if self.mtg_set.value < other.mtg_set.value:
            return True
        if self.mtg_set.value == other.mtg_set.value:
            if self.rarity.value < other.rarity.value:
                return True
            if self.rarity.value == other.rarity.value:
                if self.color.value < other.color.value:
                    return True
        return False


def get_random_color_common():
    x = random.randint(1, 81) - 1
    if x < 1:
        return Color.GOLD
    if x < 1 + 5:
        return Color.COLORLESS
    return Color(random.randint(Color.WHITE.value, Color.GREEN.value))


def get_random_color_common2():
    x = random.randint(1, 81) - 1
    if x < 2 * (1):
        return Color.GOLD
    if x < 2 * (1 + 5):
        return Color.COLORLESS
    return Color(random.randint(Color.WHITE.value, Color.GREEN.value))


def get_random_color_uncommon():
    x = random.randint(1, 100) - 1
    if x < 10:
        return Color.GOLD
    if x < 10 + 5:
        return Color.COLORLESS
    return Color(random.randint(Color.WHITE.value, Color.GREEN.value))


def get_random_color_rare():
    x = random.randint(1, 60) - 1
    if x < 16:
        return Color.GOLD
    if x < 16 + 5:
        return Color.COLORLESS
    return Color(random.randint(Color.WHITE.value, Color.GREEN.value))


def get_random_color_mythic():
    return Color.ANY


def get_pack():
    cards = []
    # Cards 1-6: Common (at least 1 of each color?)
    cards.append(Card(Rarity.COMMON, Color.WHITE))
    cards.append(Card(Rarity.COMMON, Color.BLUE))
    cards.append(Card(Rarity.COMMON, Color.BLACK))
    cards.append(Card(Rarity.COMMON, Color.RED))
    cards.append(Card(Rarity.COMMON, Color.GREEN))
    cards.append(Card(Rarity.COMMON))
    #cards.append(Card(Rarity.COMMON))
    #cards.append(Card(Rarity.COMMON))
    #cards.append(Card(Rarity.COMMON))
    #cards.append(Card(Rarity.COMMON))
    #cards.append(Card(Rarity.COMMON))

    # Card 7: Common or Special Guest
    if random.random() < 0.018:
        cards.append(Card(Rarity.MYTHIC, Color.ANY, MtgSet.SPG))
    else:
        cards.append(Card(Rarity.COMMON))

    # Cards 8-10: Uncommons
    cards.append(Card(Rarity.UNCOMMON))
    cards.append(Card(Rarity.UNCOMMON))
    cards.append(Card(Rarity.UNCOMMON))

    # Card 11: Wildcard
    r = random.random()
    if r < 0.125:
        cards.append(Card(Rarity.COMMON))
    elif r < 0.125 + 0.625:
        cards.append(Card(Rarity.UNCOMMON))
    elif r < 0.125 + 0.625 + 0.106:
        cards.append(Card(Rarity.RARE))
    elif r < 0.125 + 0.625 + 0.106 + 0.003:
        cards.append(Card(Rarity.MYTHIC))
    elif r < 0.125 + 0.625 + 0.106 + 0.003 + 0.1:
        cards.append(Card(Rarity.RARE, Color.ANY, MtgSet.EOS))
    elif r < 0.125 + 0.625 + 0.106 + 0.003 + 0.1 + 0.025:
        cards.append(Card(Rarity.MYTHIC, Color.ANY, MtgSet.EOS))
    elif r < 0.125 + 0.625 + 0.106 + 0.003 + 0.1 + 0.025 + 0.01:
        cards.append(Card(Rarity.RARE))  # TODO: viewport land
    elif r < 0.125 + 0.625 + 0.106 + 0.003 + 0.1 + 0.025 + 0.01 + 0.002:
        cards.append(Card(Rarity.MYTHIC))  # TODO: viewport land
    elif r < 0.125 + 0.625 + 0.106 + 0.003 + 0.1 + 0.025 + 0.01 + 0.002 + 0.002:
        cards.append(Card(Rarity.RARE))
    else: #  r < 0.125 + 0.625 + 0.106 + 0.003 + 0.1 + 0.025 + 0.01 + 0.002 + 0.002 + 0.002:
        cards.append(Card(Rarity.MYTHIC))

    # Card 12: Rare/Mythic
    r = random.random()
    if r < 0.804 + 0.02 + 0.02:
        cards.append(Card(Rarity.RARE))
    elif r < 0.804 + 0.02 + 0.02 + 0.142 + 0.005 + 0.005:
        cards.append(Card(Rarity.MYTHIC))
    else: # r < 0.804 + 0.02 + 0.02 + 0.142 + 0.005 + 0.005 + 0.004:
        cards.append(Card(Rarity.MYTHIC))  # TODO: viewport land

    # Card 13: Foil
    r = random.random()
    if r < 0.58:
        cards.append(Card(Rarity.COMMON))
    elif r < 0.58 + 0.32:
        cards.append(Card(Rarity.UNCOMMON))
    elif r < 0.58 + 0.32 + 0.064:
        cards.append(Card(Rarity.RARE))
    elif r < 0.58 + 0.32 + 0.064 + 0.011:
        cards.append(Card(Rarity.MYTHIC))
    elif r < 0.58 + 0.32 + 0.064 + 0.011 + 0.01:
        cards.append(Card(Rarity.RARE, Color.ANY, MtgSet.EOS))
    elif r < 0.58 + 0.32 + 0.064 + 0.011 + 0.01 + 0.005:
        cards.append(Card(Rarity.MYTHIC, Color.ANY, MtgSet.EOS))
    elif r < 0.58 + 0.32 + 0.064 + 0.011 + 0.01 + 0.005 + 0.005:
        cards.append(Card(Rarity.RARE))
    else: # r < 0.58 + 0.32 + 0.064 + 0.011 + 0.01 + 0.005 + 0.005 + 0.005:
        cards.append(Card(Rarity.MYTHIC))

    return cards


def main():
    pool = defaultdict(int)
    for _ in range(6):
        cards = get_pack()
        for card in cards:
            pool[card] += 1

    keys = sorted(pool.keys())
    for key in keys:
        print(pool[key], key)


if __name__ == '__main__':
    main()
