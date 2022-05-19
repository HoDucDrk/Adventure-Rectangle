import pygame
from Package.Entity import Entity
from Package.CONFIG import *


class Enemy(Entity):

    def __init__(self, pos, groups, obstacles_sprites, damage_player, isBoss=False):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.image = pygame.Surface((TILESIZE // 2, TILESIZE))
        if isBoss:
            self.image.fill((255, 255, 0))
        else:
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

        self.obstacles_sprites = obstacles_sprites
        # Trạng thái của kẻ địch
        self.status = 'idle'
        self.notice = False
        # chỉ số của kẻ địch
        key = 'boss' if isBoss else 'normal'
        self.health = enemy_stats[key]['health']
        self.damage = enemy_stats[key]['damage']
        self.speed = enemy_stats[key]['speed']
        self.attack_radius = enemy_stats[key]['attack_radius']
        self.notice_radius = enemy_stats[key]['notice_radius']
        #get sát thương nhận được từ player
        self.damage_player = damage_player

        #Thời gian miến nhiễm nhận dame từ player
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

    def get_player_distance_direction(self, player):
        '''
        Tìm khoảng cách của kẻ địch đến player
        '''
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec)
        Euclid_magniture = distance.magnitude() #Trả về độ lớn của vector
        #normalize trả về vector cùng hướng có độ lớn bằng 1
        self.direction = distance.normalize() if Euclid_magniture > 0 else pygame.math.Vector2()
        return Euclid_magniture, self.direction        


    def get_status(self, player):
        distance, _ = self.get_player_distance_direction(player)

        if distance <= self.attack_radius:
            self.status = 'attack'
        elif distance <= self.notice_radius or self.notice:
            self.notice = True
            self.status = 'move'
        else:
            self.status = 'idle'

    def animate(self):
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def actions(self, player):
        '''
        Set hành động cho kẻ địch
        Chú ý, tấn công và di chuyển
        '''
        if player.health <= 0:
            self.notice = False
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.damage)
        elif self.status == 'move':
            _, self.direction = self.get_player_distance_direction(player)
        else:
            self.direction = pygame.math.Vector2()

    def cooldowns(self):
        current = pygame.time.get_ticks()

        if not self.vulnerable:
            if current - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player):
        if self.vulnerable:
            _, self.direction = self.get_player_distance_direction(player)
            self.health -= player.get_full_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def update(self):
        self.move(self.speed, False)

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
        self.animate()
        self.cooldowns()
        self.check_death()
