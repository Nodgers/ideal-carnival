import pygame

from projectiles import RedLaser, SpreadLaser, HomingMissile

SPRITE_POOL = {}


class PulseShot:
    def __init__(self, main_game):
        super().__init__()
        self.fired_time = 0
        self.level = 0
        self.main_game = main_game
        self.shot_frequency = 400
        self.shot_power = 1

    def make_projectile(self, offset_x=0, offset_y=0):
        global SPRITE_POOL
        if "RedLaser" not in SPRITE_POOL:
            SPRITE_POOL["RedLaser"] = []

        projectile_pool = SPRITE_POOL["RedLaser"]

        # If there's a projectile we can use in the pool, try to use that
        if len(projectile_pool) > 0:
            for p in projectile_pool:
                # Look for one that's dead so you don't end up using a live one
                if p.is_dead:
                    p.reset(offset_x, offset_y)
                    return True

        # If there's no
        new_projectile = RedLaser(self.main_game, offset_x, offset_y)
        self.main_game.projectile_group.add(new_projectile)
        self.main_game.all_sprites_group.add(new_projectile)
        projectile_pool.append(new_projectile)

    def power_up(self):
        if self.level == 0:
            self.shot_frequency = 400
        if self.level == 1:
            self.shot_frequency = 300
        if self.level == 2:
            self.shot_frequency = 200
        if self.level == 3:
            self.shot_frequency = 100
        if self.level == 4:
            self.shot_frequency = 200
            self.shot_power = 2
        if self.level == 5:
            self.shot_frequency = 100
        if self.level == 6:
            self.shot_frequency = 100
            self.shot_power = 3
        if self.level == 7:
            self.shot_frequency = 60

        self.level += 1
        print(f"Power Up! Level {self.level}")

    def fire(self):
        if (pygame.time.get_ticks() - self.fired_time) < self.shot_frequency:
            return

        # Fire a single bullet
        self.make_projectile(0, -20)

        # Upgrade 1: Add two extra bullets
        if self.shot_power > 1:
            self.make_projectile(-10, -10)
            self.make_projectile(10, -10)

        # Upgrade 2: Add more two bullets
        if self.shot_power > 2:
            self.make_projectile(-20, 0)
            self.make_projectile(20, 0)

        self.fired_time = pygame.time.get_ticks()


class SpreadShot:
    def __init__(self, main_game):
        super().__init__()
        self.fired_time = 0
        self.level = 0
        self.main_game = main_game
        self.shot_frequency = 800
        self.shot_power = 1

    def make_projectile(self, spread=0.0):
        global SPRITE_POOL
        if "SpreadLaser" not in SPRITE_POOL:
            SPRITE_POOL["SpreadLaser"] = []

        projectile_pool = SPRITE_POOL["SpreadLaser"]

        # If there's a projectile we can use in the pool, try to use that
        if len(projectile_pool) > 0:
            for p in projectile_pool:
                # Look for one that's dead so you don't end up using a live one
                if p.is_dead:
                    p.reset(spread)
                    return True

        # If there's no
        new_projectile = SpreadLaser(self.main_game, spread)
        self.main_game.projectile_group.add(new_projectile)
        self.main_game.all_sprites_group.add(new_projectile)
        projectile_pool.append(new_projectile)

    def power_up(self):
        if self.level == 0:
            self.shot_power = 2
        if self.level == 1:
            self.shot_power = 3
        if self.level == 2:
            self.shot_power = 4
        if self.level == 3:
            self.shot_frequency = 700
        if self.level == 4:
            self.shot_frequency = 600
        if self.level == 5:
            self.shot_frequency = 500
        if self.level == 6:
            self.shot_frequency = 400
        if self.level == 7:
            self.shot_frequency = 300

        self.level += 1
        print(f"Power Up! Level {self.level}")

    def fire(self):
        if (pygame.time.get_ticks() - self.fired_time) < self.shot_frequency:
            return

        # Fire a single bullet
        self.make_projectile(-0.2)
        self.make_projectile(0.2)

        # Upgrade 1: Add two extra bullets
        if self.shot_power > 1:
            self.make_projectile(-0.6)
            self.make_projectile(0.6)

        # Upgrade 2: Add more two bullets
        if self.shot_power > 2:
            self.make_projectile(-1.0)
            self.make_projectile(1.0)

        if self.shot_power > 3:
            self.make_projectile(-0.4)
            self.make_projectile(0.4)

        if self.shot_power > 4:
            self.make_projectile(-0.8)
            self.make_projectile(0.8)

        self.fired_time = pygame.time.get_ticks()


class HomingMissileLauncher:
    def __init__(self, main_game):
        super().__init__()
        self.fired_time = 0
        self.level = 0
        self.main_game = main_game
        self.shot_frequency = 2000
        self.shot_power = 1

    def make_projectile(self, offset_x=0.0, offset_y=0.0):
        global SPRITE_POOL
        if "HomingMissile" not in SPRITE_POOL:
            SPRITE_POOL["HomingMissile"] = []

        projectile_pool = SPRITE_POOL["HomingMissile"]

        # If there's a projectile we can use in the pool, try to use that
        if len(projectile_pool) > 0:
            for p in projectile_pool:
                # Look for one that's dead so you don't end up using a live one
                if p.is_dead:
                    p.reset(offset_x, offset_y)
                    return True

        # If there's no
        new_projectile = HomingMissile(self.main_game, offset_x, offset_y)
        self.main_game.projectile_group.add(new_projectile)
        self.main_game.all_sprites_group.add(new_projectile)
        projectile_pool.append(new_projectile)

    def power_up(self):
        if self.level == 0:
            self.shot_frequency = 1000
        if self.level == 1:
            self.shot_frequency = 900
        if self.level == 2:
            self.shot_frequency = 800
        if self.level == 3:
            self.shot_frequency = 700
        if self.level == 4:
            self.shot_frequency = 600
        if self.level == 5:
            self.shot_frequency = 500
        if self.level == 6:
            self.shot_frequency = 400
        if self.level == 7:
            self.shot_frequency = 300

        self.level += 1
        print(f"Power Up! Level {self.level}")

    def fire(self):
        if (pygame.time.get_ticks() - self.fired_time) < self.shot_frequency:
            return

        self.make_projectile(-20)
        self.make_projectile(20)

        self.fired_time = pygame.time.get_ticks()
