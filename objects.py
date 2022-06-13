from position import Position
from enum import Enum
import pygame
import random


class GameObject:
    _position = None
    _display = True

    def __init__(self, x, y):
        self.__position = Position(x, y)

    def get_x(self):
        return self.__position.get_x()

    def get_y(self):
        return self.__position.get_y()

    def get_position(self):
        return self.__position.get_position()

    def set_position(self, x, y):
        self.__position = Position(x, y)


class Action(Enum):
    MOVE_UP = 'U'
    MOVE_DOWN = 'D'
    MOVE_LEFT = 'L'
    MOVE_RIGHT = 'R'
    PICK = 'P'
    KILL = 'K'
    WAIT = 'W'


class Role(GameObject):
    __name = None
    __good_at = None
    __weapon = None
    __alive = True
    __movable = True
    __auto = True
    __game = None

    def __init__(self, x, y, name, good_at):
        super().__init__(x, y)
        self.__name = name
        self.__good_at = good_at
        if name == 'victim':
            self.__movable = False

    def get_name(self):
        return self.__name

    def is_good_at(self):
        return self.__good_at

    def get_weapon(self):
        return self.__weapon

    def pick_weapon(self, weapon):
        self.__weapon = weapon

    def is_alive(self):
        return self.__alive

    def killed(self):
        self.__alive = False

    def is_movable(self):
        return self.__movable

    def set_movable(self, movable):
        self.__movable = movable

    def set_human_play(self):
        self.__auto = False

    # take random action for AI player
    def move(self, actions):
        if self.__auto:
            index = random.randint(0, len(actions) - 1)
            return actions[index]
        else:
            mark = True
            action = None
            while mark:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit(0)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and Action.PICK in actions:
                            mark = False
                            action = Action.PICK
                        elif event.key == pygame.K_SPACE and Action.KILL in actions:
                            mark = False
                            action = Action.KILL
                        elif event.key == pygame.K_w and Action.MOVE_UP in actions:
                            mark = False
                            action = Action.MOVE_UP
                        elif event.key == pygame.K_s and Action.MOVE_DOWN in actions:
                            mark = False
                            action = Action.MOVE_DOWN
                        elif event.key == pygame.K_a and Action.MOVE_LEFT in actions:
                            mark = False
                            action = Action.MOVE_LEFT
                        elif event.key == pygame.K_d and Action.MOVE_RIGHT in actions:
                            mark = False
                            action = Action.MOVE_RIGHT
            return action

    def __str__(self):
        return 'Role: %s x=%d y=%d' % (self.__name, self.get_x(), self.get_y())


class WeaponType(Enum):
    KNIFE = 'Knife'
    ROPE = 'Rope'
    POISON = 'Poison'

    def get_type(self):
        return self.value


class Weapon(GameObject):
    __type = None
    __owner = None
    __collectable = True

    def __init__(self, x, y, weapon_type):
        super().__init__(x, y)
        self.__type = weapon_type

    def picked(self, owner):
        self._display = False
        self.__collectable = False
        self.__owner = owner

    def is_collectable(self):
        return self.__collectable

    def get_position(self):
        if self.__owner is not None:
            return self.__owner.get_position()
        return super().get_position()

    def get_type(self):
        return self.__type

    def __str__(self):
        return 'Weapon: %s x=%d y=%d' % (self.__type.get_type(), self.get_x(), self.get_y())

