from map import Map
from objects import *
from tile import *
import constant
import random


class DeadlyHotel:
    _map_code = 1
    _map = None
    _roles = []
    _weapons = []
    _role_origins = []
    _weapon_origins = []
    _turns = 0
    _records = []

    def __init__(self, turns):
        self._map_code = random.randint(constant.min_map_code, constant.max_map_code)
        self._turns = turns

    def display(self):
        print('Map:')
        print(self._map)
        for role in self._roles:
            print(role)
        print()
        for weapon in self._weapons:
            print(weapon)

    def init(self):
        self._map = Map('map/' + str(self._map_code) + '.txt')
        self._init_roles()
        self._init_weapons()

    def _init_roles(self):
        roles = 4
        names = ['cleaner', 'writer', 'waitress', 'victim']
        weapons = [WeaponType.KNIFE, WeaponType.ROPE, WeaponType.POISON, None]
        self._init_role_origins()
        for i in range(0, roles):
            index = random.randint(0, len(self._role_origins) - 1)
            x, y = self._role_origins.pop(index).get_position()
            role = Role(x, y, names[i], weapons[i])
            self._roles.append(role)

    # generate available init positions for roles
    def _init_role_origins(self):
        self._role_origins.append(Position(1, 1))  # A
        self._role_origins.append(Position(1, 4))  # B
        self._role_origins.append(Position(1, 7))  # C
        self._role_origins.append(Position(1, 10))  # D
        self._role_origins.append(Position(1, 13))  # E
        self._role_origins.append(Position(1, 16))  # F

    def _init_weapons(self):
        weapons = 3
        weapon_type = [WeaponType.KNIFE, WeaponType.ROPE, WeaponType.POISON]
        self._init_weapon_origins()
        for i in range(0, weapons):
            index = random.randint(0, len(self._weapon_origins) - 1)
            x, y = self._weapon_origins.pop(index).get_position()
            weapon = Weapon(x, y, weapon_type[i])
            self._weapons.append(weapon)

    # generate available init positions for weapons
    def _init_weapon_origins(self):
        self._weapon_origins.append(Position(6, 2))  # G
        self._weapon_origins.append(Position(6, 9))  # H
        self._weapon_origins.append(Position(6, 16))  # I

    # generate legal actions for a role
    def _get_legal_actions(self, role):
        actions = []
        if role == self._roles[3]:
            actions.append(Action.WAIT)
        else:
            x, y = role.get_position()
            # check weapon
            if role.get_weapon() is None:
                for weapon in self._weapons:
                    weapon_x, weapon_y = weapon.get_position()
                    if x == weapon_x and y == weapon_y:
                        actions.append(Action.PICK)
                        break
            # check victim
            victim = self._roles[3]
            victim_x, victim_y = victim.get_position()
            if victim.is_alive():
                if x == victim_x and y == victim_y:
                    if role.get_weapon() is not None:
                        actions.append(Action.KILL)
            # check four directions
            # left
            if y - 1 > 0:
                if self._map.get_tile_type(x, y - 1) is not TileType.WALL:
                    actions.append(Action.MOVE_LEFT)
            # right
            if y + 1 < self._map.get_cols():
                if self._map.get_tile_type(x, y + 1) is not TileType.WALL:
                    actions.append(Action.MOVE_RIGHT)
            # up
            if x - 1 > 0:
                if self._map.get_tile_type(x - 1, y) is not TileType.WALL:
                    actions.append(Action.MOVE_UP)
            # down
            if x + 1 < self._map.get_rows():
                if self._map.get_tile_type(x + 1, y) is not TileType.WALL:
                    actions.append(Action.MOVE_DOWN)
        return actions

    def _update_state(self, role, action, turn):
        victim = self._roles[3]
        if role == victim:
            return
        else:
            x, y = role.get_position()
            if action == Action.WAIT:
                return
            elif action == Action.PICK:
                for weapon in self._weapons:
                    weapon_x, weapon_y = weapon.get_position()
                    if x == weapon_x and y == weapon_y:
                        weapon.picked(role)
                        role.pick_weapon(weapon)
                        break
            elif action == Action.KILL:
                victim.killed()
                self._records.append(role.get_name() + " killed victim in turn " + str(turn))
            elif action == Action.MOVE_UP:
                role.set_position(x - 1, y)
                self.record_meeting(role, turn)
            elif action == Action.MOVE_DOWN:
                role.set_position(x + 1, y)
                self.record_meeting(role, turn)
            elif action == Action.MOVE_LEFT:
                role.set_position(x, y - 1)
                self.record_meeting(role, turn)
            elif action == Action.MOVE_RIGHT:
                role.set_position(x, y + 1)
                self.record_meeting(role, turn)

    def record_meeting(self, role, turn):
        x, y = role.get_position()
        victim = self._roles[3]
        for other_role in self._roles:
            if other_role != role and other_role != victim:
                other_x, other_y = other_role.get_position()
                if x == other_x - 1 and y == other_y:
                    self._records.append(role.get_name() + " meet " + other_role.get_name() + " in turn " + str(turn))
                if x == other_x + 1 and y == other_y:
                    self._records.append(role.get_name() + " meet " + other_role.get_name() + " in turn " + str(turn))
                if x == other_x and y == other_y + 1:
                    self._records.append(role.get_name() + " meet " + other_role.get_name() + " in turn " + str(turn))
                if x == other_x and y == other_y - 1:
                    self._records.append(role.get_name() + " meet " + other_role.get_name() + " in turn " + str(turn))

    def loop(self):
        wait_role = []
        turn = 1
        while turn < self._turns + 1:
            for role in self._roles:
                if role != self._roles[3] and role in wait_role:
                    wait_role.remove(role)
                    continue
                actions = self._get_legal_actions(role)
                action = role.move(actions)
                if action == Action.KILL and role.get_weapon().get_type() != role.is_good_at():
                    wait_role.append(role)
                self._update_state(role, action, turn)
            turn += 1

    def finish(self):
        for record in self._records:
            print(record)
