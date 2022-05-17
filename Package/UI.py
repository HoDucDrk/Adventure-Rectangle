from dis import show_code
import pygame
from Package.CONFIG import *


class UI:

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # thanh máu và đạn
        self.health_bar_rect = pygame.Rect(
            10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.number_ammo_rect = pygame.Rect(10, 34, NUMBER_AMMO, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)

    def show_number_die(self, count_die):
        text_surf = self.font.render(
            f'number of deaths: {count_die}', False, (230, 230, 230))
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         text_rect.inflate(20, 10))
        self.display_surface.blit(text_surf, text_rect)

    def show_label_die(self, cooldown):
        self.font_label = pygame.font.Font(UI_FONT, 160)
        text_surf = self.font_label.render('You Died', False, (255, 100, 100))
        x = self.display_surface.get_size()[0] // 2
        y = self.display_surface.get_size()[1] // 2
        text_rect = text_surf.get_rect(center=(x, y-50))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         text_rect.inflate(1280, 10))
        self.display_surface.blit(text_surf, text_rect)

        self.show_content(cooldown+1, (255, 100, 100))

    def show_content(self, content, color):
        self.font_label_cooldown = pygame.font.Font(UI_FONT, 80)
        time_down_surf = self.font_label_cooldown.render(f'{content}', False, color)
        x = self.display_surface.get_size()[0] // 2
        y = self.display_surface.get_size()[1] // 2
        text_rect_time = time_down_surf.get_rect(center=(x, y+80))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         text_rect_time.inflate(1280, 10))
        self.display_surface.blit(time_down_surf, text_rect_time)

    def show_label_win(self):
        self.font_label = pygame.font.Font(UI_FONT, 160)
        text_surf = self.font_label.render('You Won', True, (255, 255, 100))
        x = self.display_surface.get_size()[0] // 2
        y = self.display_surface.get_size()[1] // 2
        text_rect = text_surf.get_rect(center=(x, y-50))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         text_rect.inflate(1280, 10))
        self.display_surface.blit(text_surf, text_rect)

        self.show_content('press ESC to exits', (255, 255, 100))

    def display(self, player, count_die):
        self.show_bar(
            player.health, player_stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.number_ammo,
                      player_stats['number_ammo'], self.number_ammo_rect, AMMO_COLOR)
        self.show_number_die(count_die)
