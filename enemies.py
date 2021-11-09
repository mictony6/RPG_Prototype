import pygame

from sprites import Enemy


class Guardian(Enemy):
    def __init__(self, pos, dimension=(64, 64), entity_id=None):
        super().__init__(pos, dimension, entity_id)
        self.id = "01"
        self.head = pygame.Rect(self.rect.right, self.rect.centery, 32, 32)
        self.frontal_image = {"front": pygame.image.load("./data/enemies/01/f_body.png").convert_alpha(),
                              "back": pygame.image.load("./data/enemies/01/b_body.png").convert_alpha()
                              }
        self.side_image = {"right": pygame.image.load("./data/enemies/01/s_body.png").convert_alpha(),
                           "left": pygame.transform.flip(
                               pygame.image.load("./data/enemies/01/s_body.png").convert_alpha(), True, False)
                           }
        self.diagonal_image = {"bottomleft": pygame.image.load("./data/enemies/01/df_body.png").convert_alpha(),
                               "bottomright": pygame.transform.flip(
                                   pygame.image.load("./data/enemies/01/df_body.png").convert_alpha(), True, False),
                               "topright": pygame.image.load("./data/enemies/01/db_body.png").convert_alpha(),
                               "topleft": pygame.transform.flip(
                                   pygame.image.load("./data/enemies/01/db_body.png").convert_alpha(), True, False)
                               }
        self.f_legs = [pygame.image.load("./data/enemies/01/f_leg_1.png").convert_alpha(),
                       pygame.image.load("./data/enemies/01/f_leg_2.png").convert_alpha(),
                       pygame.image.load("./data/enemies/01/f_leg_3.png").convert_alpha()]
        size = 128

        self.b_legs = []
        for indx, img in enumerate(self.f_legs):
            self.f_legs[indx] = pygame.transform.scale(img, (size, size))
            self.b_legs.append(self.f_legs[indx])

        self.r_legs = [pygame.image.load("./data/enemies/01/s_leg_1.png").convert_alpha(),
                       pygame.image.load("./data/enemies/01/s_leg_2.png").convert_alpha(),
                       pygame.image.load("./data/enemies/01/s_leg_3.png").convert_alpha()
                       ]
        self.l_legs = []
        for indx, img in enumerate(self.r_legs):
            self.r_legs[indx] = pygame.transform.scale(img, (size, size))
            self.l_legs.append(pygame.transform.flip(self.r_legs[indx], True, False))

        self.dbr_legs = [
                        pygame.image.load("./data/enemies/01/db_leg_1.png").convert_alpha(),
                        pygame.image.load("./data/enemies/01/db_leg_2.png").convert_alpha(),
                        pygame.image.load("./data/enemies/01/db_leg_3.png").convert_alpha()
                       ]
        self.dbl_legs = []
        for indx, img in enumerate(self.dbr_legs):
            self.dbr_legs[indx] = pygame.transform.scale(img, (size, size))
            self.dbl_legs.append(pygame.transform.flip(self.dbr_legs[indx], True, False))
        self.dfl_legs = [
                        pygame.image.load("./data/enemies/01/df_leg_1.png").convert_alpha(),
                        pygame.image.load("./data/enemies/01/df_leg_2.png").convert_alpha(),
                        pygame.image.load("./data/enemies/01/df_leg_3.png").convert_alpha()
                       ]
        self.dfr_legs =[]
        for indx, img in enumerate(self.dfl_legs):
            self.dfl_legs[indx] = pygame.transform.scale(img, (size, size))
            self.dfr_legs.append(pygame.transform.flip(self.dfl_legs[indx], True, False))

        for key in self.frontal_image.keys():
            self.frontal_image[key] = pygame.transform.scale(self.frontal_image[key], (size, size))
        for key in self.side_image.keys():
            self.side_image[key] = pygame.transform.scale(self.side_image[key], (size, size))
        for key in self.diagonal_image.keys():
            self.diagonal_image[key] = pygame.transform.scale(self.diagonal_image[key], (size, size))
        self.image = self.side_image["right"]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect
        self.frame_index = 0
        self.animation_speed = 5 / 60
        self.legs = self.f_legs

    def animate(self):
        if not self.reached_target:
            self.frame_index += self.animation_speed
        if self.frame_index >= len(self.legs):
            self.frame_index = 0

        if self.facing_down:

            self.legs = self.f_legs
            if self.facing_left:
                self.legs = self.dfl_legs
                self.image = self.diagonal_image["bottomleft"]
            elif self.facing_right:
                self.legs = self.dfr_legs
                self.image = self.diagonal_image["bottomright"]
            else:
                self.image = self.frontal_image["front"]
                self.legs = self.f_legs

        elif self.facing_up:

            self.legs = self.b_legs
            if self.facing_left:
                self.legs = self.dbl_legs
                self.image = self.diagonal_image["topleft"]
            elif self.facing_right:
                self.legs = self.dbr_legs
                self.image = self.diagonal_image["topright"]
            else:
                self.legs = self.b_legs
                self.image = self.frontal_image["back"]

        if self.facing_right and not (self.facing_up or self.facing_down):
            self.image = self.side_image["right"]
            self.legs = self.r_legs

        if self.facing_left and not (self.facing_up or self.facing_down):
            self.image = self.side_image["left"]
            self.legs = self.l_legs

    def __repr__(self):
        return "Guardian"
