# Imports
import sys
import time

from pygame.locals import *

# Initializing
from base_classes import *
from enemies import *

# Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Background:
    def __init__(self, main_game):
        self.bg_image = pygame.image.load('images/backgrounds/Background.png')
        self.rect_bg_img = self.bg_image.get_rect()
        self.main_game = main_game

        # Position an image, Y2 on top of Y1
        self.bg_y1 = 0
        self.bg_x1 = 0

        self.bg_y2 = -self.rect_bg_img.height
        self.bg_x2 = 0

        self.moving_up_speed = 1

    def update(self):
        # Scroll the images both down
        self.bg_y1 += self.moving_up_speed
        self.bg_y2 += self.moving_up_speed

        # Once the bottom image is fully off-screen, put it back on top
        if self.bg_y1 >= self.rect_bg_img.height:
            self.bg_y1 = -self.rect_bg_img.height
        if self.bg_y2 >= self.rect_bg_img.height:
            self.bg_y2 = -self.rect_bg_img.height

    def render(self):
        self.main_game.display_surface.blit(self.bg_image, (self.bg_x1, self.bg_y1))
        self.main_game.display_surface.blit(self.bg_image, (self.bg_x2, self.bg_y2))


class MainGame:
    def __init__(self):
        self.score_drops = None
        self.score = 0
        self.game_over = None
        self.font_small = None
        self.font = None
        pygame.init()

        self.all_sprites_group = None
        self.background = None
        self.display_surface = None
        self.enemy_group = None
        self.enemy_types = None
        self.fps = None
        self.framePerSec = None
        self.player1 = None
        self.player_group = None
        self.power_up_group = None
        self.projectile_group = None
        self.screen_height = None
        self.screen_width = None
        self.spawn_enemy = None
        self.spawn_power_up = None

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

        # Setting up Fonts
        self.font = pygame.font.SysFont("Impact", 60)
        self.font_small = pygame.font.SysFont("Impact", 20)

        # Scores to render
        self.score_drops = []

    def create_groups(self):
        # Creating Sprites Groups
        self.enemy_group = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()
        self.power_up_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.all_sprites_group = pygame.sprite.Group()

    def setup_game(self):
        # Create background
        self.background = Background(self)

        # Setting up Sprites
        self.player1 = Player(self)
        self.all_sprites_group.add(self.player1)

        # Spawn Enemy event every 1000ms
        self.spawn_enemy = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_enemy, 1000)

        self.enemy_types = [EasyEnemy, MediumEnemy, HardEnemy]

    def end_game(self):
        # Everything that happens when the player dies
        self.display_surface.fill(RED)
        game_over = self.font.render("GAME OVER", True, BLACK)
        self.display_surface.blit(game_over, (50, self.screen_height / 2))

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
                if event.type == self.spawn_enemy:  # TODO: Replace with match case when Python 3.10 lands
                    # Spawn random enemy
                    random.choice(self.enemy_types)(self)

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # Draw the background
            self.background.update()
            self.background.render()

            # Draw the scores
            scores = self.font_small.render(str(self.score), True, WHITE)
            self.display_surface.blit(scores, (10, 10))

            # Moves and Re-draws all Sprites
            for entity in self.all_sprites_group:
                self.display_surface.blit(entity.image, entity.rect)
                entity.move()
                entity.update()

            # Render all the scores
            dead_score_drops = []
            for score_drop in self.score_drops:
                score_drop.update()
                if score_drop.age > score_drop.lifespan:
                    dead_score_drops.append(score_drop)
                    continue
                score_drop.render()

            # Clean up any old score drops so they don't keep rendering
            for i in reversed(dead_score_drops):
                del(i)

            pygame.display.update()
            self.framePerSec.tick(self.fps)


if __name__ == "__main__":
    mainGame = MainGame()
    mainGame.start()
