
import time
import math
import random
from typing import List
import pygame as pg


class Config:
    SCREEN_HEIGHT = 600
    SCREEN_WIDTH = 900
    TANK_HEIGHT = int(0.05 * SCREEN_HEIGHT)
    TANK_WIDTH = int(0.05 * SCREEN_WIDTH)
    FLOOR_HEIGHT = int(0.95 * SCREEN_HEIGHT)
    TANK_SPEED = 0.2
    GRAVITY = 0.002
    JUMP_SPEED = -1.2
    PROJECTILE_RADIUS = 10
    PROJECTILE_SPEED = -2.0
    COOLDOWN = 10


def is_in_the_floor(object):
    return (object.py + object.h) >= (Config.FLOOR_HEIGHT)


class TankConfig:
    ANGLE_SPEED = 0.1
    GUN_LINE_WIDTH = 5
    TANK_LINE_WIDTH = 5
    GUN_SIZE = 50
    ANGLE_LIMIT = 90


class Tank:
    def __init__(self, p0_x, p0_y, height, width, tank_color):
        self.px = p0_x
        self.py = p0_y
        self.h = height
        self.w = width
        self.v_x = 0
        self.v_y = 0
        self.angle_gun = random.randint(-90, 0)
        self.angle_v = 0  # TankConfig.ANGLE_SPEED
        self.color = tank_color
        self.n_hits = 0
        self.cooldown = 0

    def draw(self, screen):
        # draw the tank
        pg.draw.rect(
            screen,
            self.color,
            pg.rect.Rect(self.px, self.py, self.w, self.h),
            TankConfig.TANK_LINE_WIDTH
        )

        # draw the gun
        (st_x, st_y), (end_x, end_y) = self.gun_position()
        pg.draw.line(
            screen,
            self.color,
            (st_x, st_y),
            (end_x, end_y),
            TankConfig.GUN_LINE_WIDTH
        )

    def gun_position(self):
        dx, dy = self.gun_direction()
        dx *= TankConfig.GUN_SIZE
        dy *= TankConfig.GUN_SIZE
        st_x = self.px + (self.w // 2)
        st_y = self.py
        end_x = st_x - dx
        end_y = st_y - dy
        return (st_x, st_y), (end_x, end_y)

    def gun_direction(self):
        a_rad = math.radians(self.angle_gun)
        dx = math.sin(a_rad)
        dy = math.cos(a_rad)
        return (dx, dy)

    def update(self, screen_width, floor_position, gravity):
        # update the gun angle
        self.angle_gun -= self.angle_v

        if self.angle_gun > 10:
            self.angle_gun = 10
        if self.angle_gun <= -TankConfig.ANGLE_LIMIT:
            self.angle_gun = -TankConfig.ANGLE_LIMIT

        # update the tank horizontal position
        self.px += self.v_x
        if self.px < 0:
            self.px = 0

        limit_x = (screen_width - self.w)
        if self.px > limit_x:
            self.px = limit_x

        # update the tank vertical position
        self.py += self.v_y
        self.v_y += gravity
        if is_in_the_floor(self):
            self.v_y = 0
            self.py = floor_position - self.h

        # update cooldown time
        self.cooldown -= 1
        if self.cooldown == 0:
            self.cooldown = 0


class Projectile:
    def __init__(self, p0_x, p0_y, color, radius):
        self.px = p0_x
        self.py = p0_y
        self.v_x = 0
        self.v_y = 0
        self.h = self.r = radius
        self.color = color

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.px, self.py), self.r)

    def update(self, screen_width, floor_position, gravity):
        # update the tank horizontal position
        self.px += self.v_x
        if self.px < 0:
            self.px = 0

        limit_x = (screen_width - self.r)
        if self.px > limit_x:
            self.px = limit_x

        # update the tank vertical position
        self.py += self.v_y
        self.v_y += gravity
        if is_in_the_floor(self):
            self.v_y = 0
            self.py = floor_position - self.r


class Target:
    def __init__(self, p0_x, p0_y, radius):
        TARGET_SPEED = 0.2
        self.px = p0_x
        self.py = p0_y
        self.v_y = TARGET_SPEED
        self.h = self.r = radius
        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.px, self.py), self.r)

    def update(self, screen_width, floor_position, gravity):
        # update the tank vertical position
        self.py += self.v_y
        if (self.py >= Config.SCREEN_HEIGHT) or (self.py <= 0):
            self.v_y = -self.v_y


def perform_shot(player: Tank, projectiles):
    print("perform shot")
    _, (x, y) = player.gun_position()
    dir_x, dir_y = player.gun_direction()
    new_projectile = Projectile(
        x, y, player.color, Config.PROJECTILE_RADIUS)
    new_projectile.v_x = player.v_x + Config.PROJECTILE_SPEED * dir_x
    new_projectile.v_y = player.v_y + Config.PROJECTILE_SPEED * dir_y
    projectiles.append(new_projectile)


def update_game_objects(objects):
    for o in objects:
        o.update(
            Config.SCREEN_WIDTH,
            Config.FLOOR_HEIGHT,
            Config.GRAVITY
        )


def remove_objects_in_the_floor(projectiles):
    new_list = []

    for o in projectiles:
        if not is_in_the_floor(o):
            new_list.append(o)

    return new_list


def draw_objects(screen, objects, font, n_hits, time_remaining):
    screen.fill((255, 255, 255))

    # draw the floor
    rect = pg.rect.Rect(
        0,
        Config.FLOOR_HEIGHT,
        Config.SCREEN_WIDTH,
        Config.SCREEN_HEIGHT
    )

    pg.draw.rect(
        screen,
        (153, 51, 0),
        rect
    )

    # draw objects
    for o in objects:
        o.draw(screen)

    # draw score
    img = font.render(
        f'{time_remaining:.0f} - {n_hits}', True, (0, 0, 0))

    screen.blit(img, (Config.SCREEN_WIDTH * 0.45, 20))

    pg.display.flip()


def circle_rectangle_collision_test(circle, rect):
    DeltaX = circle.px - max(rect.px, min(circle.px, rect.px + rect.w))
    DeltaY = circle.py - max(rect.py, min(circle.py, rect.py + rect.h))
    return (DeltaX * DeltaX + DeltaY * DeltaY) < (circle.r * circle.r)


def circle_circle_collision_test(circle_1, circle_2):
    centers_d = math.sqrt(
        (circle_1.px - circle_2.px) ** 2 +
        (circle_1.py - circle_2.py) ** 2
    )

    sum_rads = circle_1.r + circle_2.r

    return centers_d < sum_rads


def test_collisions(projectiles, targets):
    n_hits = 0

    projectiles_collided = []
    targets_collided = []

    for p in projectiles:
        for t in targets:
            if circle_circle_collision_test(p, t):
                n_hits += 1
                projectiles_collided.append(p)
                targets_collided.append(t)

    projectiles[:] = [p for p in projectiles if p not in projectiles_collided]
    targets[:] = [t for t in targets if t not in targets_collided]

    return n_hits


def add_targets(objects):
    objects.append(Target(
        random.randint(int(0.75 * Config.SCREEN_WIDTH),
                       int(0.95 * Config.SCREEN_WIDTH)),
        random.randint(0, Config.SCREEN_HEIGHT),
        20
    ))


def main():
    pg.init()

    screen = pg.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))

    TANK_INITIAL_Y = Config.FLOOR_HEIGHT - Config.TANK_HEIGHT

    player_1 = Tank(
        int(Config.SCREEN_WIDTH * 0.1),
        TANK_INITIAL_Y,
        Config.TANK_HEIGHT,
        Config.TANK_WIDTH,
        (255, 0, 0)
    )

    projectiles = []
    targets = []

    font = pg.font.SysFont(None, 48)
    finish_game = False

    n_hits = 0
    time_remaining = 60

    ref = time.time()

    add_targets(targets)

    # main loop
    while not finish_game:
        update_game_objects([player_1] + projectiles + targets)

        time_remaining -= time.time() - ref
        ref = time.time()

        projectiles = remove_objects_in_the_floor(projectiles)
        n_collisions = test_collisions(projectiles, targets)
        n_hits += n_collisions

        if n_collisions > 0:
            add_targets(targets)

        draw_objects(screen, [player_1] + projectiles +
                     targets, font, n_hits, time_remaining)

        # event handling, gets all event from the event queue
        for event in pg.event.get():
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_w)) or (pg.key.get_pressed()[pg.K_w]):
                player_1.angle_v = -TankConfig.ANGLE_SPEED
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_s)) or (pg.key.get_pressed()[pg.K_s]):
                player_1.angle_v = TankConfig.ANGLE_SPEED
            if ((event.type == pg.KEYUP) and (event.key == pg.K_w)) or \
                    ((event.type == pg.KEYUP) and (event.key == pg.K_s)):
                player_1.angle_v = 0

            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_e)) or (pg.key.get_pressed()[pg.K_e]):
                perform_shot(player_1, projectiles)

                # only do something if the event is of type QUIT
            if (event.type == pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                finish_game = True


if __name__ == "__main__":
    main()
