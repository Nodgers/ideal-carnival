import pygame

from base_classes import Enemy


class EasyEnemy(Enemy):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.image.load("images/enemies/EasyEnemy.png")
        self.health = 1


class MediumEnemy(Enemy):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.image.load("images/enemies/MediumEnemy.png")
        self.health = 3
        self.chance_to_drop = 1


class HardEnemy(Enemy):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.image.load("images/enemies/HardEnemy.png")
        self.health = 5
        self.chance_to_drop = 3
