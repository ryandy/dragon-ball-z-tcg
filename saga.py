import sys


class Saga:
    SAIYAN = 1

    @staticmethod
    def to_string(saga):
        return {Saga.SAIYAN: 'saiyan',
                }[saga]
