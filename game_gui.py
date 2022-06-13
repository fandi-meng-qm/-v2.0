import pygame
import constant
import random
from tile import *
from objects import *
from game import DeadlyHotel


class DeadlyHotelGUI(DeadlyHotel):
    __window = None
    __window_width = 0
    __window_height = 0
    __tile_img = []
    __role_img = []
    __role_armed_img = []
    __role_dead_img = []
    __role_display = []
    __weapon_img = []
    __role = None

    def __init__(self, turns):
        super().__init__(turns)

    def init(self):
        pygame.init()
        super().init()
        index = random.randint(0, len(self._roles) - 2)
        self.__role = self._roles[index]
        self.__role.set_human_play()
        self.__init_window()
        self.__init_images()
        self.__draw_map()
        self.__draw_roles()
        self.__draw_weapons()
        self.__draw_info()
        pygame.display.update()

    def __init_window(self):
        self.__window_width = self._map.get_cols() * constant.tile_width
        self.__window_height = self._map.get_rows() * constant.tile_height + 200
        self.__window = pygame.display.set_mode((self.__window_width, self.__window_height))
        pygame.display.set_caption("Deadly Hotel")
        self.__window.fill(constant.white)

    def __init_images(self):
        for i in range(0, 4):
            self.__tile_img.append(pygame.image.load('img/tile_' + str(i) + '.png').convert_alpha())
            self.__role_img.append(pygame.image.load('img/role_' + str(i) + '.png').convert_alpha())
            self.__role_armed_img.append(pygame.image.load('img/armed_' + str(i) + '.png').convert_alpha())
            self.__role_dead_img.append(pygame.image.load('img/armed_' + str(i) + '.png').convert_alpha())
        for i in range(0, 3):
            self.__weapon_img.append(pygame.image.load('img/weapon_' + str(i) + '.png').convert_alpha())
            self.__weapon_img[i].set_colorkey(constant.white)

    def __draw_map(self):
        for i in range(0, self._map.get_rows()):
            for j in range(0, self._map.get_cols()):
                tile = self._map.get_tile_type(i, j)
                index = 0
                if tile == TileType.WALL:
                    index = 0
                elif tile == TileType.DOOR:
                    index = 1
                elif tile == TileType.ROOM:
                    index = 2
                elif tile == TileType.CORRIDOR:
                    index = 3
                self.__window.blit(self.__tile_img[index], (constant.tile_width * j, constant.tile_height * i))

    def __draw_roles(self):
        self.__role_display = []
        for i in range(0, len(self._roles)):
            role = self._roles[i]
            x, y = role.get_position()
            if not role.is_alive():
                self.__role_display.append(self.__role_dead_img[i])
            else:
                if role.get_weapon() is not None:
                    self.__role_display.append(self.__role_armed_img[i])
                else:
                    self.__role_display.append(self.__role_img[i])
            self.__role_display[i].set_colorkey(constant.white)
            self.__window.blit(self.__role_display[i], (constant.tile_width * y, constant.tile_height * x))

    def __draw_weapons(self):
        for i in range(0, len(self.__weapon_img)):
            weapon = self._weapons[i]
            if weapon.is_collectable():
                x, y = weapon.get_position()
                self.__window.blit(self.__weapon_img[i], (constant.tile_width * y, constant.tile_height * x))

    def __draw_info(self):
        text_begin_height = self._map.get_rows() * constant.tile_height + 10
        font = pygame.freetype.SysFont('cambria', 20)
        surface, rect = font.render('Triangle stands for cleaner, who is good at using knife.', constant.black)
        self.__window.blit(surface, (10, text_begin_height + 0 * constant.font_height))
        surface, rect = font.render('Square stands for writer, who is good at using rope.', constant.black)
        self.__window.blit(surface, (10, text_begin_height + 1 * constant.font_height))
        surface, rect = font.render('Circle stands for waitress, who is good at using poison.', constant.black)
        self.__window.blit(surface, (10, text_begin_height + 2 * constant.font_height))
        surface, rect = font.render('Star stands for victim, who can not move.', constant.black)
        self.__window.blit(surface, (10, text_begin_height + 3 * constant.font_height))
        surface, rect = font.render('You are ' + self.__role.get_name(), constant.red)
        self.__window.blit(surface, (10, text_begin_height + 4 * constant.font_height))
        surface, rect = font.render('WASD for moving, SPACE for pick up weapon or kill.', constant.blue)
        self.__window.blit(surface, (10, text_begin_height + 5 * constant.font_height))

    def update_gui(self):
        self.__draw_map()
        self.__draw_roles()
        self.__draw_weapons()
        pygame.display.update()

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
            self.update_gui()

    def finish_gui(self):
        # TODO
        return

    def finish(self):
        super().finish()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    break


gui = DeadlyHotelGUI(50)
gui.init()
gui.loop()
gui.finish()
