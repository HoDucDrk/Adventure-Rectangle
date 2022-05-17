import pygame
from Package.CONFIG import *


class Tile(pygame.sprite.Sprite):

    def __init__(self, pos, groups, isFinishLine=False):
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        if isFinishLine:
            self.sprite_type = 'finish_line'
            self.image.fill((0, 255, 255))
        else:
            self.sprite_type = 'wall'
            self.image.fill((20, 20, 20))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -20)
