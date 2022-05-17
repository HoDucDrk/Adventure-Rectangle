import pygame
from Package.CONFIG import *
from Package.Tile import Tile
from Package.Player import Player
from Package.Enemy import Enemy
from Package.Bullet import Bullet
from Package.UI import UI


class Level:

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        # nhóm có thể nhìn thấy
        self.visible_sprites = YSortCameraGroup()
        # nhóm chướng ngại vật
        self.obstacles_sprites = pygame.sprite.Group()
        # cản đường đạn
        self.bulletproof = pygame.sprite.Group()
        # Nhóm các vật phẩm có thể tấn công
        self.attack_sprites = pygame.sprite.Group()
        # Nhóm có thể tấn công
        self.attackable_sprites = pygame.sprite.Group()

        self.count_die = 0
        # Giao diện
        self.ui = UI()
        # Load map
        self.create_map()
        # hồi sinh nhân vật
        self.respam_delay = None
        self.respam = True
        self.respam_cooldown = 5000

    def create_map(self):
        '''Khởi tạo các đối tượng mặc định trong file csv'''
        map_data = {
            'wall': load_map('./Assets/Map/Map_Map.csv'),
            'enemy': load_map('./Assets/Map/Map_Object.csv'),
            'linewin': load_map('./Assets/Map/Map_linewin.csv')
        }

        for style, layout in map_data.items():
            for i in range(layout.shape[0]):
                for j in range(layout.shape[1]):
                    if layout[i, j] != -1:
                        x = j * TILESIZE
                        y = i * TILESIZE
                        if style == 'wall':
                            Tile(pos=(x, y), 
                                 groups=[self.visible_sprites, self.obstacles_sprites, self.bulletproof])
                        if style == 'linewin':
                            Tile(pos=(x, y), 
                                 groups=[self.visible_sprites, self.obstacles_sprites, self.bulletproof], 
                                 isFinishLine=True)
                        if style == 'enemy':
                            if layout[i, j] == 5:
                                self.enemy = Enemy(pos=(x, y),
                                                   groups=[self.visible_sprites, self.attackable_sprites, self.bulletproof],
                                                   obstacles_sprites=self.obstacles_sprites,
                                                   damage_player=self.damage_player)
                            elif layout[i, j] == 2:
                                self.enemy = Enemy(pos=(x, y),
                                                   groups=[self.visible_sprites, self.attackable_sprites, self.bulletproof],
                                                   obstacles_sprites=self.obstacles_sprites,
                                                   damage_player=self.damage_player,
                                                   isBoss=True)
                            else:
                                self.player = Player(
                                    (x, y), [self.visible_sprites], self.obstacles_sprites, self.create_attack)

    def create_attack(self):
        '''Khởi tạo tấn công từ lớp Bullet'''
        self.current_attack = Bullet(self.player, [self.visible_sprites, self.attack_sprites], self.bulletproof, self.enemy)
        self.current_attack.update()

    def dead_character(self):
        '''
        Khi máu nhân vật xuống dưới không thì 
        loại bỏ sprite nhân vật ra khỏi tất cả các Group liên quan
        '''
        if self.player.health <= 0:
            self.player.kill()
            if self.respam:
                self.respam = False
                self.respam_delay = pygame.time.get_ticks()
                self.count_die += 1

    def cooldown_respame(self):
        '''
        Thực hiện đếm ngược khi nhân vật chết.
        Khi thời gian đếm ngược kết thúc khởi tạo lại nhân vật
        '''
        current = pygame.time.get_ticks()

        if not self.respam and self.player.health <= 0:
            time_down = self.respam_cooldown - int(current - self.respam_delay)
            self.ui.show_label_die(time_down // 1000)
            
            if current - self.respam_delay >= self.respam_cooldown:
                self.player = Player(
                    (30, 30), [self.visible_sprites], self.obstacles_sprites, self.create_attack)
                self.respam = True

    def damage_player(self, amount):
        '''
        Giảm máu của nhân vật khi bị kẻ địch đánh phải.
        Trong một khoảng thời gian nhân vật sẽ miễn nhận sát thương
        '''
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damage(self.player)

    def check_won(self):
        if self.player.finished:
            self.ui.show_label_win()

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.enemy_update(self.player)
        self.visible_sprites.update()
        self.player_attack_logic()
        self.cooldown_respame()
        self.dead_character()
        self.check_won()
        self.ui.display(self.player, self.count_die)


class YSortCameraGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Tạo nền
        self.floor_surf = pygame.Surface((TILESIZE * 50, TILESIZE * 30))
        self.floor_surf.fill((0, 255, 0))
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        # Hiển thị nền
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
