world_data = [

    '                         ',
    '   P E                   ',
    '  XXXXX        XXXXXX    ',
    '  XXXXX           XXX    ',
    '        XXXXXX           ',
    'XXX     XXXXXXX    XXXXXX',
    'XXXXXX     XXXX     XXXX ',
    '   XXX     XXXX     XXXX ',
    'X          XXXX     XXXX ',
    'XX    XXX           XXXX ',
    'XXX  XXXXXX   dXXXXXXXXXX',
    'XXX  XXXXXX   XXXXXXXXXXX',

]
tile_size = 128
screen_width = 720
screen_height = 720
p_speed = 2
p_speed *= 2


class Tracker:
    def __init__(self, speed=p_speed):
        self.speed = speed
        self.slow = speed // 2
        self.fast = speed

    def track(self, key, state=False):
        if state and key == "walk":
            self.speed = self.slow
            return self.speed
        if not state:
            self.speed = self.fast
            return self.speed

    def get_speed(self):
        return self.speed

    def get_slow(self):
        return self.slow


tracker = Tracker(p_speed)
