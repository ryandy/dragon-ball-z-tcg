import sys

from card_factory import CardFactory
from saga import Saga


def main():
    goku1 = CardFactory.from_spec(Saga.SAIYAN, 158)
    goku2 = CardFactory.from_spec(Saga.SAIYAN, 159)
    print(goku1)
    print(goku2)


if __name__ == '__main__':
    main()
