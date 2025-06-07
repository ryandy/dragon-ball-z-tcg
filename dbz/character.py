import enum
import sys


class Character(enum.Enum):
    GOKU = 1
    PICCOLO = 2
    GOHAN = 3
    KRILLIN = 4
    RADITZ = 5
    VEGETA = 6
    NAPPA = 7
    TIEN = 8
    YAMCHA = 9
    CHI_CHI = 10
    BULMA = 11
    CHIAOTZU = 12
    YAJIROBE = 13
    SAIBAIMEN = 14
    GARLIC_JR = 15
    GULDO = 16
    FRIEZA = 17
    MASTER_ROSHI = 18
    VIDEL = 19
    BABA = 20
    KING_KAI = 21

    @classmethod
    def from_str(cls, s):
        s = s.upper()
        s = s.replace('-', '_')
        s = s.replace(' ', '_')
        return cls[s]

    def has_saiyan_heritage(self):
        return self in [
            Character.GOKU,
            Character.VEGETA,
            Character.GOHAN,
            Character.RADITZ,
            Character.NAPPA]

    def has_namekian_heritage(self):
        return self in [
            Character.PICCOLO]

    def can_steal_dragon_balls(self):
        return self in [
            Character.BULMA,
            Character.KRILLIN,
            Character.SAIBAIMEN,
            Character.CHI_CHI,
            Character.TIEN,
            Character.YAMCHA,
            Character.GARLIC_JR,
            Character.GULDO,
            Character.FRIEZA,
            Character.MASTER_ROSHI,
            Character.VIDEL]
