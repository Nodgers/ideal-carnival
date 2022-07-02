import random
import pygame


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, main_game, spawn_pos):
        super().__init__()
        self.main_game = main_game

        self.image = pygame.image.load("images/items/PowerUp.png")
        self.rect = self.image.get_rect()
        self.rect.center = spawn_pos

        self.speed = 1
        self.main_game.power_up_group.add(self)
        self.main_game.all_sprites_group.add(self)

    def update(self):
        player = pygame.sprite.spritecollideany(self, self.main_game.player_group)
        if player:
            self.main_game.player1.power += 1
            self.kill()

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > self.main_game.screen_height:
            # If the enemy reaches the bottom without getting killed, despawn it
            self.kill()


class ScoreDrop:
    def __init__(self, parent):
        self.font_render = None
        self.parent = parent
        self.position = list(parent.rect.center)
        self.creation_time = pygame.time.get_ticks()
        self.age = 0
        self.lifespan = 1000
        self.font = pygame.font.SysFont("Impact", 24)

    def update(self):
        self.position[1] += self.parent.speed
        self.age = pygame.time.get_ticks() - self.creation_time


    def render(self):
        self.font_render = self.font.render(f"+{self.parent.score_value}", True, (255, 255, 255))


class Enemy(pygame.sprite.Sprite):
    """
    - Enemy -
    Base class for all enemies
    """

    def __init__(self, main_game):
        super().__init__()
        self.main_game = main_game

        self.image = pygame.image.load("images/enemies/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, self.main_game.screen_width - 40), 0)

        self.health = 1
        self.speed = 5
        self.chance_to_drop = 0  # 0 in 50 times chance to drop powerup
        self.getting_hit_by = []
        self.score_value = 1

        self.main_game.enemy_group.add(self)
        self.main_game.all_sprites_group.add(self)

    def update(self):
        colliding_entity = pygame.sprite.spritecollideany(self, self.main_game.projectile_group)
        if colliding_entity is not None:
            if colliding_entity not in self.getting_hit_by:
                self.getting_hit_by.append(colliding_entity)
                self.health -= 1
                if self.health < 1:
                    self.die()
                else:
                    colliding_entity.kill()
        else:
            self.getting_hit_by = []

    def die(self):
        # Roll dice for drop
        pick = random.randint(1, 20)

        # Roll another dice for every chance to drop
        for chance in range(self.chance_to_drop):
            if random.randint(1, 20) == pick:
                # If you managed to pick the right number, spawn a power up at the enemy's location
                PowerUp(self.main_game, self.rect.center)

        # Add to game score
        self.main_game.score += self.score_value

        # Drop score
        score_drop = ScoreDrop(self)
        self.main_game.score_drops.append(score_drop)

        self.kill()

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > 600:
            # If the enemy reaches the bottom without getting killed, despawn it
            self.kill()


class PlayerProjectile(pygame.sprite.Sprite):
    """
    - Player_Projectile -
    Base class for all player projectiles
    """

    def __init__(self, main_game, offset):
        super().__init__()
        self.main_game = main_game
        self.image = pygame.image.load("images/weapons/Projectile.png")
        self.rect = self.image.get_rect()
        self.rect.center = self.main_game.player1.rect.center
        self.rect.move_ip(offset, 0)
        self.speed = 10
        self.main_game.projectile_group.add(self)
        self.main_game.all_sprites_group.add(self)

    def move(self):
        self.rect.move_ip(0, self.speed * -1)
        if self.rect.top < 0:
            self.kill()


class Player(pygame.sprite.Sprite):
    """
    - Player -
    Base class for all player character
    """

    def __init__(self, main_game):
        super().__init__()
        self.main_game = main_game
        self.getting_hit = False
        self.image = pygame.image.load("images/players/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        self.health = 1
        self.power = 1
        self.fire_delta = 100
        self.main_game.player_group.add(self)
        self.main_game.all_sprites_group.add(self)
        self.fired_time = 0

    def make_projectile(self, offset=0):
        new_projectile = PlayerProjectile(self.main_game, offset)
        self.main_game.projectile_group.add(new_projectile)
        self.main_game.all_sprites_group.add(new_projectile)

    def fire(self):
        # Fire a single bullet
        self.make_projectile()

        # Upgrade 1: Add two extra bullets
        if self.power > 1:
            self.make_projectile(-10)
            self.make_projectile(10)

        # Upgrade 2: Add a further two bullets
        if self.power > 2:
            self.make_projectile(-20)
            self.make_projectile(20)

        self.fired_time = pygame.time.get_ticks()

    def take_damage(self, amount):
        self.health -= amount

    def update(self):
        # Check to see if the player is getting hit by any enemies
        check_enemy_collision = pygame.sprite.spritecollideany(self, self.main_game.enemy_group)
        if check_enemy_collision:
            if not self.getting_hit:
                self.getting_hit = True
                self.take_damage(1)
                if self.health < 1:
                    self.die()
                else:
                    check_enemy_collision.kill()
        else:
            self.getting_hit = False

        # Check for fire button
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_SPACE]:
            fire_time_delta = pygame.time.get_ticks() - self.fired_time
            if fire_time_delta > self.fire_delta:
                self.fire()

    def die(self):
        self.kill()
        self.main_game.end_game()

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < self.main_game.screen_width:
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)
        if self.rect.top > 0:
            if pressed_keys[pygame.K_UP]:
                self.rect.move_ip(0, -5)
        if self.rect.bottom < self.main_game.screen_height:
            if pressed_keys[pygame.K_DOWN]:
                self.rect.move_ip(0, 5)
