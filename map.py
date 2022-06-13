from position import Position
from tile import Tile, TileType


class Map:
    __map = []
    __rows = 0
    __cols = 0

    def __init__(self, path):
        if not self.__load_map(path):
            print('Wrong map file.')
            quit(1)

    def __load_map(self, path):
        with open(path, 'r') as file:
            try:
                line = file.readline()
                self.__rows = int(line)
                line = file.readline()
                self.__cols = int(line)
            except ValueError:
                return False
            try:
                for i in range(0, self.__rows):
                    self.__map.append([])
                    line = file.readline()
                    if len(line) < self.__cols:
                        return
                    for j in range(0, self.__cols):
                        code = line[j:j+1]
                        self.__map[i].append(Tile(i, j, TileType.get_type(code)))
            except ValueError:
                return False
        return True

    def get_rows(self):
        return self.__rows

    def get_cols(self):
        return self.__cols

    def get_tile_type(self, x, y):
        return self.__map[x][y].get_type()

    def __str__(self):
        value = ''
        for i in range(0, self.__rows):
            for j in range(0, self.__cols):
                value += self.__map[i][j].get_type().get_code()
            value += '\n'
        return value
