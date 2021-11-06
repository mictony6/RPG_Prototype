world_data = [

    '                         ',
    '   P E                   ',
    '  XXXXX        XXXXXX    ',
    '  XXXXX           XXX    ',
    '        XXXXXX      E    ',
    'XXX     XXXXXXX    XXXXXX',
    'XXXXXX     XXXX     XXXX ',
    '   XXX     XXXX     XXXX ',
    'X      E   XXXX     XXXX ',
    'XX    XXX       E   XXXX ',
    'XXX  XXXXXX   dXXXXXXXXXX',
    'XXX  XXXXXX   XXXXXXXXXXX',

]
tile_size = 128
screen_width = 1280
screen_height = 720
p_speed = 1
p_speed *= 2
debugging = 0
frame = 1 / 60  # average
world_size = (len(world_data[1])*tile_size, len(world_data)*tile_size)
i_count = 0


class Tracker:
    def __init__(self, speed=p_speed):
        self.speed = speed
        self.slow = speed // 2
        self.fast = speed
        self.weapon_index = 0
        self.vx = 0
        self.vy = 0
        self.countx = 0
        self.county = 0

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

    def get_weapon_index(self):
        old = self.weapon_index
        if old >= 2:
            self.weapon_index = 0
        self.weapon_index += .1
        return (old)





tracker = Tracker(p_speed)
