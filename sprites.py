import random
from abc import abstractmethod
from math import sqrt

import pygame as pygame
from config import tracker, screen_height, screen_width, world_size


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.Surface((64, 64))
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))
        self.hitbox = self.image.get_rect(topleft=(pos[0], pos[1]))
        self.image.fill('red')
        self.weapon_image = None
        self.weapon_rect = None

        # collision statuses
        self.collide_r = False
        self.collide_l = False
        self.collide_t = False
        self.collide_b = False
        self.scrolled = {"up": False, "down": False, "left": False, "right": False}
        self.actions = {"idle": True, "attacking": False, "run": False, "attacked": False, "stagger": False}
        self.facing_right = True
        self.facing_left = False

        # x and y velocity..change in displacement over time
        self.velocity = pygame.math.Vector2(0, 0)
        # axis direction
        self.direction = pygame.math.Vector2(0, 0)

        # player/entity status
        self.health = 100
        self.stamina = 100
        self.money = 0
        self.hunger = 100
        self.power = 5
        self.defense = 5
        self.attack_rate = 10
        self.collision_objects = {}

    @abstractmethod
    def move(self, dx, dy):
        pass

    def move_single_axis(self, dx, dy):
        # Move the rect

        self.hitbox.x += dx
        self.hitbox.y += dy
        move_rect = True
        count = len(self.collision_objects["tiles"].sprites())
        # If you collide with a wall, move out based on velocity
        for tile in self.collision_objects["tiles"]:
            if self.hitbox.colliderect(tile.rect):
                count -= 1
                move_rect = False

                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.hitbox.right = tile.rect.left
                    self.collide_l = True
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.hitbox.left = tile.rect.right
                    self.collide_r = True
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.hitbox.bottom = tile.rect.top
                    self.collide_b = True
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.hitbox.top = tile.rect.bottom
                    self.collide_t = True

        if move_rect:
            self.weapon_rect.x += dx
            self.weapon_rect.y += dy
            self.rect.x += dx
            self.rect.y += dy

        # set everything to false if there was no collision
        # cause we only flick them on individually everytime a collision occur
        # if nothing was flicked, then player received no collision
        if count == len(self.collision_objects["tiles"].sprites()):
            self.collide_r = self.collide_l = self.collide_t = self.collide_b = False

    def attack(self, entity):
        entity.health -= self.power
        self.stamina -= 5

    @abstractmethod
    def die(self):
        pass


class Player(Sprite):
    def __init__(self, pos, image_path=None, dimension=(128, 128)):
        super().__init__(pos)
        # inherits self.image with image_path passed in
        # currently does not use image_path since i dont have any sprite image yet
        self.image_path = image_path

        # instead, I'm using rectangle to represent the player
        # dimensions are by default 64
        # self.image is for now a flat red surface since i dont have a sprite image yet
        # self.image is tied to self.rect
        # self.rect is tied self.hitbox's bottom

        self.image = pygame.image.load("./data/player.png").convert_alpha()
        # create copies of sprite image when flipped directions
        self.flipped_image = pygame.transform.flip(self.image, True, False)
        self.image_facing_right = self.image
        # create a relative hitbox
        self.hitbox = pygame.Rect(pos[0] + dimension[0] / 4, pos[1], dimension[0] - dimension[0] * 1 / 2,
                                  dimension[1] - dimension[1] * 2 / 3)
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))
        self.rect.bottom = self.hitbox.bottom + 4
        self.weapon_image = pygame.image.load("./data/sword_0.png").convert_alpha()
        self.weapon_image = pygame.transform.scale(self.weapon_image, (40 * 2, 12 * 2))
        self.weapon_rect = self.weapon_image.get_rect(center=self.rect.center)
        # self.weapon_states = {"idle":pygame.transform.rotate(self.weapon_image,90),"attacking":self.weapon_image}
        self.weapon_animation = [
            pygame.image.load("./data/sword_0.png").convert_alpha(),
            pygame.image.load("./data/sword_1.png").convert_alpha(),
            pygame.image.load("./data/sword_2.png").convert_alpha()
        ]
        for i, image in enumerate(self.weapon_animation):
            self.weapon_animation[i] = pygame.transform.scale(image, (40 * 2, 12 * 2))

        # self.image.fill('green')

    def move(self, dx, dy):

        # if player is trying to move in screenspace to the, let it move
        # move in world space
        # compute for collision and apply transformation
        if dx != 0:
            self.move_single_axis(dx, 0)
        # else if it is trying to move in world space
        # move it or predict it's supposed movement to compute for collision
        # then add or subtract it back to it's static state in screenspace
        # when the player's center is no longer making the world move
        # player's velocity would return to normal
        elif dx == 0 and (self.scrolled["left"]):
            self.move_single_axis(-tracker.get_speed(), 0)
            self.hitbox.x += tracker.get_speed()
            self.rect.x += tracker.get_speed()
            self.weapon_rect.x += tracker.get_speed()

        elif dx == 0 and (self.scrolled["right"]):
            self.move_single_axis(tracker.get_speed(), 0)
            self.hitbox.x -= tracker.get_speed()
            self.rect.x -= tracker.get_speed()
            self.weapon_rect.x -= tracker.get_speed()

        if dy != 0:
            self.move_single_axis(0, dy)
        elif dy == 0 and self.scrolled["up"]:
            self.move_single_axis(0, -tracker.get_speed())
            self.hitbox.y += tracker.get_speed()
            self.rect.y += tracker.get_speed()
            self.weapon_rect.y += tracker.get_speed()

        elif dy == 0 and self.scrolled["down"]:
            self.move_single_axis(0, tracker.get_speed())
            self.hitbox.y -= tracker.get_speed()
            self.rect.y -= tracker.get_speed()
            self.weapon_rect.y -= tracker.get_speed()

    def combat(self, enemy_list):
        pressed = pygame.key.get_pressed()
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.hitbox):
                if self.direction.x > 0:  # Moving right; Hit the left side of the enemy
                    self.move(-tracker.get_speed(), 0)
                if self.direction.x < 0:  # Moving left; Hit the right side of the enemy
                    self.move(tracker.get_speed(), 0)
                if self.direction.y > 0:  # Moving down; Hit the top side of the enemy
                    self.move(0, -tracker.get_speed())
                if self.direction.y < 0:  # Moving up; Hit the bottom side of the enemy
                    self.move(0, tracker.get_speed())

                if pressed[pygame.K_e] and self.actions["idle"]:
                    self.attack(enemy)
                    print(f"Attacking enemy.\nEnemy health:{enemy.health}")
                    self.actions["idle"] = False
                    self.actions["attacking"] = True
                    if enemy.health <= 0:
                        print("Enemy is dead!")
                elif self.actions["attacking"]:
                    enemy.combat(self)
                    self.attack_rate -= .75
            if self.attack_rate <= 0:
                self.actions["idle"] = True
                self.actions["attacking"] = False
                self.attack_rate = 10

    def push(self, directionx, directiony):
        # directions says where to push player not where player is facing
        if directionx == "left":
            self.move(-20, 0)
        elif directionx == "right":
            self.move(20, 0)
        if directiony == "up":
            self.move(0, -20)
        elif directiony == "down":
            self.move(0, 20)
        self.actions["stagger"] = True

    def get_input(self):
        # horizontal movement
        pressed = pygame.key.get_pressed()
        tracker.track("walk", pressed[pygame.K_LSHIFT])
        if pressed[pygame.K_e]:
            self.actions["attacking"] = True
        else:
            self.actions["attacking"] = False
        if pressed[pygame.K_d]:
            self.image = self.image_facing_right
            self.move(self.velocity.x, 0)
            self.direction.x = 1
            self.facing_right = True
            self.facing_left = False
        if pressed[pygame.K_a]:
            self.image = self.flipped_image
            self.move(-self.velocity.x, 0)
            self.direction.x = -1
            self.facing_left = True
            self.facing_right = False

        # vertical movement
        if pressed[pygame.K_w]:
            self.move(0, -self.velocity.y)
            self.direction.y = -1

        if pressed[pygame.K_s]:
            self.move(0, self.velocity.y)
            self.direction.y = 1

        if not pressed[pygame.K_d] and not pressed[pygame.K_a]:
            self.direction.x = 0
        if not pressed[pygame.K_w] and not pressed[pygame.K_s]:
            self.direction.y = 0

    def draw_weapon(self, screen):
        index = tracker.get_weapon_index()
        image = self.weapon_animation[int(index)]

        if self.facing_right:
            self.weapon_rect.left = self.rect.right - self.rect.w / 3
            self.weapon_image = self.weapon_animation[1]
        else:
            self.weapon_rect.right = self.rect.left + self.rect.w / 3
            image = pygame.transform.flip(image, True, False)
            self.weapon_image = pygame.transform.flip(self.weapon_animation[1], True, False)

        if self.actions["attacking"]:
            self.weapon_image = image

        screen.blit(self.weapon_image, self.weapon_rect.topleft)

    def die(self):
        self.image.fill("red")

    def update(self, tiles, enemies):
        if self.health <= 0:
            self.die()
        else:
            if self.actions["idle"] and not self.actions["stagger"] and self.health < 100:
                self.health += .15

            # get input if player is not staggering
            self.collision_objects = {"tiles": tiles, "enemies": enemies}
            if not self.actions["stagger"]:
                self.get_input()
                self.combat(enemies)
            else:
                self.attack_rate -= .5
                if self.attack_rate <= 0:
                    self.actions["stagger"] = False

            if self.actions["attacked"]:
                print(f"Your Health: {self.health}")
                self.actions["attacked"] = False


# ------------------------------------------
# -----------------------------------------------------------------------------------------------
class Enemy(Sprite):
    def __init__(self, pos, image_path=None, dimension=(64, 64), entity_id=None):
        super().__init__(pos)
        self.count_trails = 0
        self.image_path = image_path
        self.rect = pygame.Rect(pos[0], pos[1], dimension[0], dimension[1])
        self.hitbox = self.rect
        self.range = self.rect.copy().inflate(128*4, 128*4)
        self.radius = self.range.w//2
        self.patience = 60*5
        self.reached_target = False
        self.current_position = self.rect.center
        self.target = (random.randrange(self.range.left, self.range.right), random.randrange(self.range.top, self.range.bottom))

        self.image.fill("lightblue")
        self.id = entity_id
        self.attack_rate = 5
        self.type = {"01": "base enemy"}

    def move(self, dx, dy):
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        # Move the rect

        self.rect.x += dx
        self.rect.y += dy

        move_rect = True
        count = len(self.collision_objects["tiles"].sprites())
        # If you collide with a wall, move out based on velocity
        for tile in self.collision_objects["tiles"]:
            if self.hitbox.colliderect(tile.rect):
                count -= 1
                move_rect = False

                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.hitbox.right = tile.rect.left
                    self.collide_l = True
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.hitbox.left = tile.rect.right
                    self.collide_r = True
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.hitbox.bottom = tile.rect.top
                    self.collide_b = True
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.hitbox.top = tile.rect.bottom
                    self.collide_t = True

        if move_rect:
            self.range.center = self.rect.center

        # set everything to false if there was no collision
        # cause we only flick them on individually everytime a collision occur
        # if nothing was flicked, then player received no collision
        if count == len(self.collision_objects["tiles"].sprites()):
            self.collide_r = self.collide_l = self.collide_t = self.collide_b = False

    def combat(self, player):
        if player.actions["attacking"] and player.attack_rate % self.attack_rate == 0:
            print("Enemy attacks back")
            self.attack(player)
            if player.direction.x > 0:
                player.push("left", "None")
            elif player.direction.x < 0:
                player.push("right", "None")
            if player.direction.y > 0:
                player.push("None", "up")
            elif player.direction.y < 0:
                player.push("None", "down")
            player.actions["attacked"] = True

    def generate_movement(self,player):
        frame = 1 / 60
        distance = sqrt((player.hitbox.centerx-self.rect.centerx)**2+(player.hitbox.centery-self.rect.centery)**2)
        if distance <= self.radius:
                self.target = player.rect.center
                self.found_player =  True
        else:
            self.found_player = False
        if self.patience <= 1 and not self.found_player:
            print('generating new target')
            self.target = (random.randrange(self.range.left, self.range.right), random.randrange(self.range.top, self.range.bottom))
            self.patience = 60*5
            self.current_position = self.rect.center

            print(self.current_position,"to",self.target)

        else:
            self.reached_target = False
            self.current_position = self.rect.center
            self.patience -= 1
            self.scan(self.target)
            if self.current_position == self.rect.center:
                self.reached_target = True




    def scan(self, target):
        if self.reached_target:
            vx =vx = 0
        else:
            vx = vy =1

        # print(dist, v)
        if self.range.centerx < target[0]:
            self.move(vx, 0)

        elif self.range.centerx > target[0]:
            self.move(-vx, 0)

        if self.collide_r or self.collide_l:

            if self.rect.centery < target[1]:
                self.move(0, 1)
            elif self.rect.centery < target[1]:
                self.move(0, -1)

        if self.range.centery > target[1]:
            self.move(0, -vy)
        elif self.range.centery < target[1]:
            self.move(0, vy)
        if self.collide_t or self.collide_b:
            if self.rect.centerx < target[0]:
                self.move(1,0)
            elif self.rect.centerx < target[0] :
                self.move(-1,0)

    def die(self):
        self.kill()
        return self.id

    def update(self, world_shift, player, tiles):
        self.collision_objects = {"tiles": tiles, "enemies": player}
        if self.health <= 0:
            print("You killed a", self.type[self.die()])
            player.attack_rate = 10
            player.actions["idle"] = True
            player.actions["attacking"] = False
        else:
            # self.combat(player)
            self.rect.center += world_shift
            self.target = (self.target[0]+world_shift[0],self.target[1]+world_shift[1])
            self.range.center+= world_shift
            self.generate_movement(player)
