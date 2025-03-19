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
