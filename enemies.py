import pygame

from baseClasses import Enemy


class EasyEnemy(Enemy):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.image.load("EasyEnemy.png")
        self.health = 1


class MediumEnemy(Enemy):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.image.load("MediumEnemy.png")
        self.health = 3
        self.chance_to_drop = 1


class HardEnemy(Enemy):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.image.load("HardEnemy.png")
        self.health = 5
        self.chance_to_drop = 3
