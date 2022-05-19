from os import stat
import pygame
from Package.CONFIG import *


class Bullet(pygame.sprite.Sprite):

    def __init__(self, player, groups, bulletproof, enemy):
        super().__init__(groups)
        self.sprite_type = 'bullet'
        direction = player.bullet_direction
        self.direction = direction
        self.speed_bullet = 25
        self.create_bullet(player, direction)

        self.enemy = enemy
        self.player = player
        self.bulletproof = bulletproof

    def create_bullet(self, player, direction):
        if direction == 'right' or direction == 'left':
            self.image = pygame.Surface((10, 5))
            self.image.fill(BULLET_COLOR)
            if direction == 'right':
                x, y = player.rect.midright
                self.rect = self.image.get_rect(midright=(x, y))
            else:
                x, y = player.rect.midleft
                self.rect = self.image.get_rect(midleft=(x, y))
        else:
            self.image = pygame.Surface((5, 10))
            self.image.fill(BULLET_COLOR)
            if direction == 'up':
                x, y = player.rect.midtop
                self.rect = self.image.get_rect(midtop=(x, y))
            else:
                x, y = player.rect.midbottom
                self.rect = self.image.get_rect(midbottom=(x, y))

    def bulletproof_collision(self):
        """
        Xử lý đạn khi đạn chạm vào vật thể
        """
        for sprite in self.bulletproof:
            if sprite.rect.colliderect(self.rect):
                if sprite.sprite_type == 'enemy':
                    sprite.notice = True
                self.kill()

    def move_bullet(self, direction):
        if direction == 'right' or direction == 'left':
            if direction == 'right':
                self.rect.x += self.speed_bullet
            else:
                self.rect.x -= self.speed_bullet
        else:
            if self.direction == 'up':
                self.rect.y -= self.speed_bullet
            else:
                self.rect.y += self.speed_bullet
        # Xử lý đường đạn khi đến một khoảng cách nào đó
        bullet_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(self.player.rect.center)
        if (bullet_vec - player_vec).magnitude() >= self.player.range_attack * TILESIZE:
            self.kill()

    def update(self):
        self.bulletproof_collision()
        self.move_bullet(self.direction)
