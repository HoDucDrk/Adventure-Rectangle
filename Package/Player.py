import sys
import pygame
from Package.Entity import Entity
from Package.CONFIG import *


class Player(Entity):

    def __init__(self, pos, groups, obstacles_sprites, create_attack):
        super().__init__(groups)

        self.sprite_type = 'player'
        # Tạo hình ảnh nhân vật
        self.image = pygame.Surface((TILESIZE // 2, TILESIZE))
        self.image.fill(CHARACTER_COLOR)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -5)

        self.obstacles_sprites = obstacles_sprites

        # Khởi tạo trạng thái mặc định
        self.status = 'down'
        self.bullet_direction = 'down'

        # Thiết lập chỉ số nhân vật
        self.health = player_stats['health']
        self.number_ammo = player_stats['number_ammo']
        self.attack = player_stats['attack']
        self.speed = player_stats['speed']
        self.range_attack = player_stats['range_attack']

        # Set delay của nhận sát thương
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        # Khởi tạo tấn công
        self.create_attack = create_attack
        self.can_attack = True
        self.attack_cooldown = 500
        self.attack_time = None

    def input(self):
        '''
        Khởi tạo các phím di chuyển nhân vật
        '''
        keys = pygame.key.get_pressed()

        self.direction.y = - \
            1 if keys[pygame.K_w] else 1 if keys[pygame.K_s] else 0
        self.direction.x = - \
            1 if keys[pygame.K_a] else 1 if keys[pygame.K_d] else 0
        if keys[pygame.K_SPACE] and self.can_attack and self.number_ammo > 0:
            self.number_ammo -= 1
            self.can_attack = False
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()

        if keys[pygame.K_ESCAPE] and self.finished:
            pygame.quit()
            sys.exit()

    def set_direction_bullet(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_l]:
            self.bullet_direction = 'right'
        elif keys[pygame.K_LEFT]  or keys[pygame.K_j]:
            self.bullet_direction = 'left'
        elif keys[pygame.K_UP]  or keys[pygame.K_i]:
            self.bullet_direction = 'up'
        elif keys[pygame.K_DOWN]  or keys[pygame.K_k]:
            self.bullet_direction = 'down'

    def cooldowns(self):
        '''
        Thời gian cooldown của tấn công và nhận sát thương của nhân vật
        '''
        current_time = pygame.time.get_ticks()

        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def set_status(self):
        if self.direction.x == -1:
            self.status = 'left'
        elif self.direction.x == 1:
            self.status = 'right'
        elif self.direction.y == -1:
            self.status = 'up'
        elif self.direction.y == 1:
            self.status = 'down'

    def get_full_damage(self):
        '''
        Tính lượng sát thương gây ra cho kẻ địch 
        '''
        base_damage = player_stats['attack']
        return base_damage

    def update(self):
        self.input()
        self.set_direction_bullet()
        self.cooldowns()
        self.animate()
        self.move(self.speed, True)
        self.set_status()
