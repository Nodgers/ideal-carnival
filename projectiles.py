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
