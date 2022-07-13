import sys
import time

from pygame.locals import *

from base_classes import *
from enemies import *
from waves import ALL_WAVES
from weapons import PulseShot, HomingMissileLauncher

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
        pygame.init()

        self.all_sprites_group = None
        self.background = None
        self.current_wave = None
        self.display_surface = None
        self.enemy_group = None
        self.enemy_types = None
        self.font = None
        self.font_small = None
        self.fps = None
        self.framePerSec = None
        self.game_over = None
        self.next_stage = None
        self.player1 = None
        self.player_group = None
        self.power_up_group = None
        self.projectile_group = None
        self.score_drops = None
        self.screen_height = None
        self.screen_width = None
        self.spawn_enemy = None
        self.spawn_power_up = None

        self.enemy_spawn_frequency = 1000
        self.next_stage_frequency = 30000  # 30 seconds
        self.score = 0
        self.orbs = 0
        self.stage = 0

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
        self.font = pygame.font.SysFont("Menlo", 60)
        self.font_small = pygame.font.SysFont("Menlo", 30)

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
        self.player1.add_weapon(PulseShot(self))
        self.player1.add_weapon(HomingMissileLauncher(self))

        self.all_sprites_group.add(self.player1)
        self.spawn_enemy = pygame.USEREVENT + 1

        self.go_to_next_stage()

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

    def go_to_next_stage(self):
        if self.stage > len(ALL_WAVES) - 1:
            print("Ran out of stages! Game over until you get off your arse and make more")
            self.end_game()

        self.current_wave = ALL_WAVES[self.stage]
        print(f"Start Wave No. {self.current_wave.wave_no} - {self.current_wave.wave_text}")

        # Spawn Enemy event every n seconds
        pygame.time.set_timer(self.spawn_enemy, self.current_wave.spawn_frequency)

        self.stage += 1

    def start(self):
        # Game Loop
        while True:
            # Cycles through all events occurring
            for event in pygame.event.get():
                if event.type == self.spawn_enemy:  # TODO: Replace with match case when Python 3.10 lands
                    # If you've spawned every enemy in the wave, move onto the next
                    current_wave_length = len(self.current_wave.enemies) - 1
                    if self.current_wave.current_enemy > current_wave_length:
                        self.go_to_next_stage()
                    else:
                        # Spawn the next enemy
                        new_enemy = self.current_wave.enemies[self.current_wave.current_enemy](self)
                        self.enemy_group.add(new_enemy)
                        new_enemy.dice_sides = current_wave_length
                        new_enemy.speed *= self.current_wave.enemy_speed_multiplier
                        self.current_wave.current_enemy += 1

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # Draw the background
            self.background.update()
            self.background.render()

            # Draw the scores
            scores = self.font_small.render(f"Score: {self.score}", True, WHITE)
            self.display_surface.blit(scores, (self.screen_width / 40, self.screen_height / 60))

            # Draw the orb count
            orbs = self.font_small.render(f"Orbs: {self.orbs}", True, WHITE)
            self.display_surface.blit(orbs, (self.screen_width / 40, (self.screen_height / 60) + 40))

            # Moves and Re-draws all Sprites
            for entity in self.all_sprites_group:
                self.display_surface.blit(entity.image, entity.rect)
                entity.move()
                entity.update()

            # Render all the score drops
            dead_score_drops = []
            for score_drop in self.score_drops:
                score_drop.update()
                if score_drop.age > score_drop.lifespan:
                    dead_score_drops.append(score_drop)
                    continue
                score_drop.render()

            # Clean up any old score drops, so they don't keep rendering
            for i in reversed(dead_score_drops):
                del(i)

            pygame.display.update()
            self.framePerSec.tick(self.fps)


if __name__ == "__main__":
    mainGame = MainGame()
    mainGame.start()
