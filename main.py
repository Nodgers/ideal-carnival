# Imports
import random
import sys
import time

from pygame.locals import *

# Initializing
from baseClasses import *
from enemies import *

# Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class MainGame:
    def __init__(self):
        pygame.init()

        self.all_sprites_group = None
        self.display_surface = None
        self.enemy_group = None
        self.enemy_types = None
        self.spawn_power_up = None
        self.power_up_group = None
        self.fps = None
        self.framePerSec = None
        self.player1 = None
        self.projectile_group = None
        self.screen_height = None
        self.screen_width = None
        self.spawn_enemy = None

        self.setup_display()
        self.create_groups()
        self.setup_game()

    def setup_display(self):
        # Setting up FPS
        self.fps = 60
        self.framePerSec = pygame.time.Clock()

        # Other Variables for use in the program
        self.screen_width = 400
        self.screen_height = 600

        # Create a white screen
        self.display_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.display_surface.fill(WHITE)

        # Name the window
        pygame.display.set_caption("Game")

    def create_groups(self):
        # Creating Sprites Groups
        self.enemy_group = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()
        self.power_up_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.all_sprites_group = pygame.sprite.Group()

    def setup_game(self):
        # Setting up Sprites
        self.player1 = Player(self)
        self.all_sprites_group.add(self.player1)

        # Spawn Enemy event every 1000ms
        self.spawn_enemy = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_enemy, 1000)

        self.enemy_types = [EasyEnemy, MediumEnemy, HardEnemy]

    def end_game(self):
        print("Game Over")
        self.display_surface.fill(RED)
        pygame.display.update()
        for entity in self.all_sprites_group:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    def start(self):
        # Game Loop
        while True:
            # Cycles through all events occuring
            for event in pygame.event.get():
                # TODO: Replace with match case when Python 3.10 lands
                if event.type == self.spawn_enemy:
                    # Spawn random enemy
                    random.choice(self.enemy_types)(self)

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # Draw the surface
            self.display_surface.fill(BLACK)

            # Moves and Re-draws all Sprites
            for entity in self.all_sprites_group:
                self.display_surface.blit(entity.image, entity.rect)
                entity.move()
                entity.update()

            pygame.display.update()
            self.framePerSec.tick(self.fps)


if __name__ == "__main__":
    mainGame = MainGame()
    mainGame.start()
