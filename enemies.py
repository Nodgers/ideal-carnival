import pygame

from base_classes import Enemy


class EasyEnemy(Enemy):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.image.load("images/enemies/EasyEnemy.png")
        self.health = 1
        self.score_value = 10


class MediumEnemy(Enemy):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.image.load("images/enemies/MediumEnemy.png")
        self.speed = 3
        self.health = 5
        self.chance_to_drop = 1
        self.score_value = 50


class HardEnemy(Enemy):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.image.load("images/enemies/HardEnemy.png")
        self.speed = 2
        self.health = 10
        self.chance_to_drop = 3
        self.score_value = 100
