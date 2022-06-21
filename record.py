from enum import Enum


class EventType(Enum):
    MEET = 0
    DEATH = 1


class RoleType(Enum):
    CLEANER = 'cleaner'
    WRITER = 'writer'
    WAITRESS = 'waitress'
    VICTIM = 'victim'

    def __str__(self):
        return self.value

    def get_code(self):
        if self == RoleType.CLEANER:
            return 0
        elif self == RoleType.WRITER:
            return 1
        elif self == RoleType.WAITRESS:
            return 2
        elif self == RoleType.VICTIM:
            return 3


class Record:
    _event = None
    _position = None
    _turn = None

    def __init__(self, position, turn):
        self._position = position
        self._turn = turn

    def get_type(self):
        return self._event

    def get_position(self):
        return self._position

    def get_turn(self):
        return self._turn


class DeathRecord(Record):
    __weapon = None

    def __init__(self, position, turn, weapon):
        super().__init__(position, turn)
        self._event = EventType.DEATH
        self.__weapon = weapon

    def get_weapon(self):
        return self.__weapon

    def __str__(self):
        return 'victim was killed by ' + str(self.__weapon) \
               + ' at ' + str(self._position) + ' in turn ' + str(self._turn)


class MeetRecord(Record):
    __role_a = None
    __role_b = None

    def __init__(self, position, turn, role_a, role_b):
        super().__init__(position, turn)
        self._event = EventType.MEET
        self.__role_a = role_a
        self.__role_b = role_b

    def __str__(self):
        return str(self.__role_a) + " meet " + str(self.__role_b) \
               + " at " + str(self._position) + ' in turn ' + str(self._turn)

    def get_role_a(self):
        return self.__role_a

    def get_role_b(self):
        return self.__role_b

