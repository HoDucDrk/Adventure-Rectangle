import pygame
import sys
import Package.CONFIG as CONFIG
from Package.Level import Level


class Window:
    
    def __init__(self):      
        pygame.init()
        pygame.display.set_caption('Adventure Rectangle')
        display_size = (CONFIG.WIDTH, CONFIG.HEIGHT)
        self.screen = pygame.display.set_mode(display_size)
        self.clock = pygame.time.Clock()
        self.level = Level()

    def __call__(self):
        while True:
            self.clock.tick(CONFIG.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.screen.fill(CONFIG.BLACK)
            self.level.run()
            pygame.display.update()