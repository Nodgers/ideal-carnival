import pygame

from base_classes import Enemy


class EasyEnemy(Enemy):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.image.load("images/enemies/EasyEnemy.png")
        self.speed = 3
        self.health = 1
        self.score_value = 10
        self.chance_to_drop = 1


class MediumEnemy(Enemy):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.image.load("images/enemies/MediumEnemy.png")
        self.speed = 3
        self.health = 3
        self.chance_to_drop = 1
        self.score_value = 50


class HardEnemy(Enemy):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.image.load("images/enemies/HardEnemy.png")
        self.speed = 2
        self.health = 5
        self.chance_to_drop = 1
        self.score_value = 100


class Boss(Enemy):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.image.load("images/enemies/Boss.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.main_game.screen_width / 2, 0)
        self.speed = 1
        self.health = 500
        self.chance_to_drop = 1
        self.score_value = 5000