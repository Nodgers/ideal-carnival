import random

from enemies import *


class Wave:
    def __init__(self, wave_no=0, wave_text=""):
        self.wave_no = wave_no
        self.wave_text = wave_text
        self.enemy_list = {}
        self.enemies = []
        self.chance_to_drop = 1
        self.enemy_speed_multiplier = 1.0
        self.spawn_frequency = 1000
        self.current_enemy = 0

    def build_enemy_list(self):
        for enemy, amount in self.enemy_list.items():
            for i in range(amount):
                self.enemies.append(enemy)

        random.shuffle(self.enemies)


"""
ALL WAVES
"""
ALL_WAVES = []

"""
Wave 1
"""
WAVE1 = Wave(1, "Welcome")
WAVE1.enemy_list = {EasyEnemy: 30}
WAVE1.chance_to_drop = 0
WAVE1.spawn_frequency = 1000
WAVE1.build_enemy_list()
ALL_WAVES.append(WAVE1)

"""
Wave 2
"""
WAVE2 = Wave(2, "Getting Started")
WAVE2.enemy_list = {EasyEnemy: 20, MediumEnemy: 3}
WAVE2.chance_to_drop = 1
WAVE2.spawn_frequency = 500
WAVE2.enemy_speed_multiplier = 1.1
WAVE2.build_enemy_list()
ALL_WAVES.append(WAVE2)

"""
Wave 3
"""
WAVE3 = Wave(3, "Let's Go")
WAVE3.enemy_list = {EasyEnemy: 30, MediumEnemy: 10, HardEnemy: 5}
WAVE2.spawn_frequency = 400
WAVE3.chance_to_drop = 0
WAVE3.build_enemy_list()
ALL_WAVES.append(WAVE3)

"""
Wave 4
"""
WAVE4 = Wave(4, "Bring it on")
WAVE4.enemy_list = {EasyEnemy: 10, MediumEnemy: 10, HardEnemy: 2}
WAVE4.chance_to_drop = 1
WAVE4.build_enemy_list()
ALL_WAVES.append(WAVE4)

"""
Wave 5
"""
WAVE5 = Wave(5, "BLAT")
WAVE5.enemy_list = {EasyEnemy: 50}
WAVE5.chance_to_drop = 1
WAVE5.spawn_frequency = 20
WAVE5.build_enemy_list()
ALL_WAVES.append(WAVE5)

"""
Wave 6
"""
WAVE6 = Wave(4, "Oh well done")
WAVE6.enemy_list = {EasyEnemy: 50, MediumEnemy: 20, HardEnemy: 10}
WAVE2.spawn_frequency = 400
WAVE6.chance_to_drop = 1
WAVE6.build_enemy_list()
ALL_WAVES.append(WAVE6)
