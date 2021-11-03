from abc import abstractmethod

import pygame as pygame
from config import tracker


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.Surface((64, 64))
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))
        self.image.fill('red')

        # collision statuses
        self.collide_r = False
        self.collide_l = False
        self.collide_t = False
        self.collide_b = False
        self.scrolled = {"up": False, "down": False, "left": False, "right": False}
        self.actions = {"idle": True, "attacking": False, "run": False, "attacked": False}

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
        self.rect.x += dx
        self.rect.y += dy
        count = len(self.collision_objects["tiles"].sprites())
        # If you collide with a wall, move out based on velocity
        for tile in self.collision_objects["tiles"]:
            if self.rect.colliderect(tile.rect):
                count -= 1
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = tile.rect.left
                    self.collide_l = True
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = tile.rect.right
                    self.collide_r = True
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = tile.rect.top
                    self.collide_b = True
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = tile.rect.bottom
                    self.collide_t = True

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
    def __init__(self, pos, image_path=None, dimension=(64, 64)):
        super().__init__(pos)
        # inherits self.image with image_path passed in
        # currently does not use image_path since i dont have any sprite image yet
        self.image_path = image_path

        # instead, I'm using rectangle to represent the player
        # dimensions are by default 32
        # self.image is for now a flat red surface since i dont have a sprite image yet
        # self.image is tied to self.rect

        self.rect = pygame.Rect(pos[0], pos[1], dimension[0], dimension[1])
        self.image = pygame.Surface((dimension[0], dimension[1]))
        # self.image = pygame.image.load("./data/player.png").convert_alpha()
        # self.image = pygame.transform.scale(self.image,(64,64))
        self.image.fill('green')

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
            self.rect.x += tracker.get_speed()

        elif dx == 0 and (self.scrolled["right"]):
            self.move_single_axis(tracker.get_speed(), 0)
            self.rect.x -= tracker.get_speed()

        if dy != 0:
            self.move_single_axis(0, dy)
        elif dy == 0 and self.scrolled["up"]:
            self.move_single_axis(0, -tracker.get_speed())
            self.rect.y += tracker.get_speed()
        elif dy == 0 and self.scrolled["down"]:
            self.move_single_axis(0, tracker.get_speed())
            self.rect.y -= tracker.get_speed()

    def combat(self, enemy_list):
        pressed = pygame.key.get_pressed()
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect):
                if self.direction.x > 0:  # Moving right; Hit the left side of the wall
                    self.move(-4, 0)
                elif self.direction.x < 0:  # Moving left; Hit the right side of the wall
                    self.move(4, 0)
                if self.direction.y > 0:  # Moving down; Hit the top side of the wall
                    self.move_single_axis(0, -4)
                elif self.direction.y < 0:  # Moving up; Hit the bottom side of the wall
                    self.move(0, 4)

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
        if directionx == "left":
            self.rect.centerx -= 40
        elif directionx == "right":
            self.rect.centerx += 40
        if directiony == "up":
            self.rect.centery -= 40
        elif directiony == "down":
            self.rect.centery += 40

    def get_input(self):
        # horizontal movement
        pressed = pygame.key.get_pressed()
        tracker.track("walk", pressed[pygame.K_LSHIFT])

        if pressed[pygame.K_d]:
            self.move(self.velocity.x, 0)
            self.direction.x = 1
        if pressed[pygame.K_a]:
            self.move(-self.velocity.x, 0)
            self.direction.x = -1

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

    def die(self):
        self.image.fill("red")

    def update(self, tiles, enemies):
        if self.health <= 0:
            self.die()
        else:
            # get key input
            self.collision_objects = {"tiles": tiles, "enemies": enemies}
            self.get_input()
            self.combat(enemies)
            if self.actions["attacked"]:
                print(f"Your Health: {self.health}")
                self.actions["attacked"] = False


class Enemy(Sprite):
    def __init__(self, pos, image_path=None, dimension=(64, 64), entity_id=None):
        super().__init__(pos)
        self.image_path = image_path
        self.rect = pygame.Rect(pos[0], pos[1], dimension[0], dimension[1])
        self.image.fill("red")
        self.id = entity_id
        self.attack_rate = 4

    def move(self, dx, dy):
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def combat(self, player):
        if player.actions["attacking"] and player.attack_rate % self.attack_rate == 0:
            print("Enemy attacks back")
            self.attack(player)
            if player.rect.centerx < self.rect.centerx:
                player.push("left", "None")
            elif player.rect.centerx > self.rect.centerx:
                player.push("right", "None")
            if player.rect.centery < self.rect.centery:
                player.push("None", "up")
            elif player.rect.centery < self.rect.centery:
                player.push("None", "down")
            player.actions["attacked"] = True
            player.actions["attacking"] = False
            player.actions["idle"] = True

    def die(self):
        self.kill()
        return self.id

    def update(self, world_shift, player):
        if self.health <= 0:
            self.die()
        else:
            # self.combat(player)
            self.rect.center += world_shift
