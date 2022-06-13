# position on the map
class Position:
    __x = 0
    __y = 0

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_position(self):
        return self.__x, self.__y

    def __str__(self):
        return 'x=%d y=%d' % (self.__x, self.__y)
