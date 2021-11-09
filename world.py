import pygame

from config import *
from enemies import Guardian
from sprites import Player
from tile import Tile, TileSlab


class World:
    def __init__(self, surface, world_map):
        # note: tiles.sprites() to iterate through every speite
        # player.sprite to access the sprite object which is Player() instance
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.display_surface = surface
        self.world_shift = pygame.math.Vector2(0, 0)
        self.count = 0
        # add tiles to tile sprite group
        # add player sprite to it's single sprite group
        # x and y placement is the ([r][c]) column index of a tile from the data multiplied by tile size
        # the tile and Player class spawns a rectangle in that position
        # added several tile types and is very messy, only concentrate on X and P conditions
        for index, row in enumerate(world_map):
            for number, placeholder in enumerate(row):
                x_placement = number * tile_size
                y_placement = index * tile_size

                # X = 64x64, can only be drawn from topleft
                # a,b,c,d,x,^,v,<,> = 32x32
                # SYSTEM:
                # a b         ^
                # c d   and < x >
                #             v
                # W,S = 64x32
                # A,D = 32x64
                # SYSTEM:
                # WW  |  AD
                # SS  |  AD

                if placeholder == "X":
                    tile = Tile((x_placement, y_placement), tile_size)
                    self.tiles.add(tile)
                elif placeholder == "a":
                    tile = TileSlab((x_placement, y_placement), pos='topleft')
                    self.tiles.add(tile)
                elif placeholder == "b":
                    tile = TileSlab((x_placement, y_placement), pos='topright')
                    self.tiles.add(tile)
                elif placeholder == "c":
                    tile = TileSlab((x_placement, y_placement), pos='bottomleft')
                    self.tiles.add(tile)
                elif placeholder == "d":
                    tile = TileSlab((x_placement, y_placement), pos='bottomright')
                    self.tiles.add(tile)
                elif placeholder == "x":
                    tile = TileSlab((x_placement, y_placement))
                    self.tiles.add(tile)
                elif placeholder == "^":
                    tile = TileSlab((x_placement, y_placement), pos='top')
                    self.tiles.add(tile)
                elif placeholder == "v":
                    tile = TileSlab((x_placement, y_placement), pos='bottom')
                    self.tiles.add(tile)
                elif placeholder == ">":
                    tile = TileSlab((x_placement, y_placement), pos='right')
                    self.tiles.add(tile)
                elif placeholder == "<":
                    tile = TileSlab((x_placement, y_placement), pos='left')
                    self.tiles.add(tile)
                elif placeholder == "W":
                    tile = TileSlab((x_placement, y_placement), (tile_size, tile_size / 2), pos='topleft')
                    self.tiles.add(tile)
                elif placeholder == "S":
                    tile = TileSlab((x_placement, y_placement), (tile_size, tile_size / 2), pos='bottomleft')
                    self.tiles.add(tile)
                elif placeholder == "A":
                    tile = TileSlab((x_placement, y_placement), (tile_size / 2, tile_size), pos='topleft')
                    self.tiles.add(tile)
                elif placeholder == "D":
                    tile = TileSlab((x_placement, y_placement), (tile_size / 2, tile_size), pos='topright')
                    self.tiles.add(tile)
                elif placeholder == "P":
                    player_sprite = Player((x_placement, y_placement))
                    self.player.add(player_sprite)
                elif placeholder == 'G':
                    enemy_sprite = Guardian((x_placement, y_placement), entity_id='01')
                    self.enemies.add(enemy_sprite)

    # noinspection DuplicatedCode,PyUnresolvedReferences
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width * (1 / 2) and direction_x < 0:
            self.world_shift.x = tracker.get_speed()
            player.velocity.x = 0
            player.scrolled["left"] = True
        elif player_x > screen_width * (1 / 2) and direction_x > 0:
            self.world_shift.x = -tracker.get_speed()
            player.velocity.x = 0
            player.scrolled["right"] = True
        else:
            self.world_shift.x = 0
            player.velocity.x = tracker.get_speed()
            player.scrolled["left"] = player.scrolled["right"] = False

    # noinspection DuplicatedCode,PyUnresolvedReferences
    def scroll_y(self):
        player = self.player.sprite
        player_y = player.rect.centery
        direction_y = player.direction.y
        if player_y < screen_height * (1 / 2) and direction_y < 0:
            self.world_shift.y = tracker.get_speed()
            player.velocity.y = 0
            player.scrolled["up"] = True
        elif player_y > screen_height * (1 / 2) and direction_y > 0:
            self.world_shift.y = -tracker.get_speed()
            player.velocity.y = 0
            player.scrolled["down"] = True
        else:
            player.scrolled["up"] = player.scrolled["down"] = False
            self.world_shift.y = 0
            player.velocity.y = tracker.get_speed()

    def run(self):
        # for debugging, displays tile rectangles with 2px width
        if debugging:
            rect_color = "green"
            if self.player.sprite.found:
                rect_color = "red"
            pygame.draw.rect(self.display_surface, "violet", self.player.sprite.hitbox, 2)
            pygame.draw.rect(self.display_surface, rect_color, self.player.sprite.rect, 2)
            pygame.draw.rect(self.display_surface, "blue", self.player.sprite.weapon_rect, 2)
        # update gets the input then moves the player's rectangle
        self.scroll_x()
        self.scroll_y()
        self.player.update(self.tiles, self.enemies)

        self.tiles.update(self.world_shift)
        self.enemies.update(self.world_shift, self.player.sprite, self.tiles, self.display_surface)
        # pygame sprite class has built in draw method
        # only needs a display surface arguement

        self.count = (self.count + 1) % 120
        # font = pygame.font.SysFont("SegoeUiVariable", 12)
        # text_surf = font.render("AREA IS CLEAR", True, 'white')
        # txt_rect = text_surf.get_rect()
        self.tiles.draw(self.display_surface)
        for tile in self.tiles.sprites():
            pygame.draw.rect(self.display_surface, 'white', tile.rect, 2)
        for enemy in self.enemies:

            self.display_surface.blit(enemy.legs[int(enemy.frame_index)],(enemy.rect.topleft))
            r = enemy.radius * (self.count / 120)
            pygame.draw.circle(self.display_surface, 'darkgreen', enemy.range.center, r, 2)
            pygame.draw.circle(self.display_surface, 'pink', enemy.range.center, enemy.radius - r // 2, 2)
            # for targets in enemy.last_found_areas:
            #     txt_rect.center = targets.coordinates
            #     pygame.draw.circle(self.display_surface,"white",targets.coordinates, 128/2, 4)
            #     self.display_surface.blit(text_surf, txt_rect.topleft)

            if debugging:
                pygame.draw.rect(self.display_surface,"orange", enemy.range, 1)
                pygame.draw.line(self.display_surface, 'red', enemy.rect.center, enemy.target, 2)
                pygame.draw.circle(self.display_surface, "orange", enemy.target, 10)
                # pygame.draw.rect(self.display_surface,"red",enemy.hitbox, 2)

        self.enemies.draw(self.display_surface)
        # for enemy in self.enemies:
        #     pygame.draw.circle(self.display_surface, "blue", enemy.head.center, 16)
        self.player.draw(self.display_surface)
        self.player.sprite.draw_weapon(self.display_surface)
