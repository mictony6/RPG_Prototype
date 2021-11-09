import random
world_data = [

    '                         ',
    '    P                    ',
    '       G                 ',
    '                         ',
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
screen_width = 1280
screen_height = 720
p_speed = 2
p_speed *= 2
frame = 1 / 60  # average
world_size = (len(world_data[1]) * tile_size, len(world_data) * tile_size)
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
        return old


tracker = Tracker(p_speed)


prob = []
tile_prob = 30
enemy_prob = 5
player_prob = 1
for n in range(tile_prob):
    prob.append("X")
for n in range(enemy_prob):
    prob.append("G")
for n in range(100-(tile_prob+enemy_prob)):
    prob.append(" ")

# [DEBUGGING]
debugging = 0
use_procedural = 0
world_width = 24
world_height = 24
# procedural generation
if debugging or use_procedural:
    world_data = []
    while len(world_data) < world_height:
        world_data.append("")
        for i in range(world_width):
            v = random.randrange(100)
            rep = prob[v]
            if len(world_data[0]) == 0:
                world_data[0] = str(world_data[0]) + "P"
                continue
            else:
                world_data[len(world_data) -
                           1] = str(world_data[len(world_data) - 1]) + rep
