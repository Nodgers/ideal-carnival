import math

import pygame


class RedLaser(pygame.sprite.Sprite):
    """
    - Player_Projectile -
    Base class for all player projectiles
    """

    def __init__(self, main_game, offset_x=0, offset_y=0):
        super().__init__()
        self.main_game = main_game
        self.image = pygame.image.load("images/weapons/Red_Laser.png")
        self.rect = self.image.get_rect()
        self.rect.center = self.main_game.player1.rect.center
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.rect.move_ip(self.offset_x, self.offset_y)
        self.speed = 10
        self.main_game.projectile_group.add(self)
        self.main_game.all_sprites_group.add(self)
        self.strength = 1
        self.is_dead = False

    def reset(self, offset_x=0, offset_y=0):
        self.is_dead = False
        self.rect = self.image.get_rect()
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.rect.center = self.main_game.player1.rect.center
        self.rect.move_ip(self.offset_x, self.offset_y)

    def move(self):
        if self.is_dead:
            return

        self.rect.move_ip(0, self.speed * -1)

        if self.rect.bottom < 0:
            self.die()

    def die(self):
        self.is_dead = True
        self.rect.center = (0, self.main_game.screen_height * -1)


class SpreadLaser(pygame.sprite.Sprite):
    """
    - Player_Projectile -
    Base class for all player projectiles
    """

    def __init__(self, main_game, spread=0.0):
        super().__init__()
        self.main_game = main_game
        self.image = pygame.image.load("images/weapons/Green_Laser.png")
        self.rect = self.image.get_rect()
        self.rect.center = self.main_game.player1.rect.center
        self.spread = spread
        self.speed = 10
        self.main_game.projectile_group.add(self)
        self.main_game.all_sprites_group.add(self)
        self.strength = 1
        self.is_dead = False

    def reset(self, spread=0.0):
        self.is_dead = False
        self.spread = spread
        self.rect = self.image.get_rect()
        self.rect.center = self.main_game.player1.rect.center

    def move(self):
        if self.is_dead:
            return

        self.rect.move_ip(self.speed * self.spread, self.speed * -1)

        if self.rect.bottom < 0:
            self.die()

    def die(self):
        self.is_dead = True
        self.rect.center = (0, self.main_game.screen_height * -1)


class HomingMissile(pygame.sprite.Sprite):
    """
    - Player_Projectile -
    Base class for all player projectiles
    """

    def __init__(self, main_game, spread=0.0):
        super().__init__()
        self.time_since_launch = 0
        self.missile_pos = pygame.math.Vector2(0, 0)
        self.main_game = main_game
        self.image = pygame.image.load("images/weapons/Missile.png")
        self.rect = self.image.get_rect()
        self.rect.center = self.main_game.player1.rect.center
        self.spread = spread
        self.speed = 10
        self.main_game.projectile_group.add(self)
        self.main_game.all_sprites_group.add(self)
        self.strength = 1
        self.is_dead = False
        self.attraction_distance = 200
        self.locked_onto = None
        self.locked_on = False
        self.velocity = pygame.math.Vector2(0, -50)
        self.launched_time = pygame.time.get_ticks()
        self.damping_constant = 0.2
        self.attraction_force = 0.1
        self.lifetime = 2000

    def reset(self, spread=0.0):
        self.image = pygame.image.load("images/weapons/Missile.png")

        self.launched_time = pygame.time.get_ticks()
        self.time_since_launch = 0
        self.velocity = pygame.math.Vector2(0, -50)
        self.locked_onto = None
        self.locked_on = False
        self.is_dead = False
        self.spread = spread
        self.rect = self.image.get_rect()
        self.rect.center = self.main_game.player1.rect.center

    def find_enemy(self):
        self.time_since_launch = (pygame.time.get_ticks() - self.launched_time)
        if self.time_since_launch < 100:
            return

        if self.time_since_launch > self.lifetime:
            self.die()

        for enemy in self.main_game.enemy_group:
            enemy_pos = pygame.math.Vector2(enemy.rect.center)
            player_pos = pygame.math.Vector2(self.main_game.player1.rect.center)
            if enemy_pos.y > player_pos.y:
                self.locked_on = False
                continue

            if enemy.is_dead:
                self.locked_on = False
                continue

            if pygame.math.Vector2(enemy.rect.center).y > self.main_game.screen_height:
                self.locked_on = False
                continue

            missile_pos = pygame.math.Vector2(self.rect.center)
            delta = enemy_pos - missile_pos
            if delta.length() < self.attraction_distance:
                self.locked_onto = enemy
                self.locked_on = True
                break

    def move(self):
        if self.is_dead:
            return

        if self.locked_on:
            if self.locked_onto.is_dead:
                self.locked_on = False
                self.locked_onto = None

        #if not self.locked_on:
        self.find_enemy()

        self.missile_pos = pygame.math.Vector2(self.rect.center)
        if self.time_since_launch < 100:
            return



        if self.locked_on:
            enemy_pos = pygame.math.Vector2(self.locked_onto.rect.center)
            delta = enemy_pos - self.missile_pos
            if delta == 0:
                self.die()
                return

            delta.normalize()
            force = pygame.math.Vector2(delta) * self.attraction_force
            force -= self.velocity * self.damping_constant
            self.velocity += force * 0.17

        angle = math.atan2(self.velocity.x, self.velocity.y) * (180 / math.pi)
        self.image = pygame.image.load("images/weapons/Missile.png")
        self.image = pygame.transform.rotate(self.image, angle)

        self.missile_pos += self.velocity * 0.17

        self.rect.center = (self.missile_pos.x, self.missile_pos.y)

        if self.rect.bottom < 0:
            self.die()

    def die(self):
        self.is_dead = True
        self.rect.center = (0, self.main_game.screen_height * -1)
