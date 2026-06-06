
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
    PROJECTILE_SPEED = -1.2
    COOLDOWN = 10


def is_in_the_floor(object):
    return (object.py + object.h) >= (Config.FLOOR_HEIGHT)


class Tank:
    def __init__(self, p0_x, p0_y, height, width, tank_color):
        ANGLE_SPEED = 0.1
        self.px = p0_x
        self.py = p0_y
        self.h = height
        self.w = width
        self.v_x = 0
        self.v_y = 0
        self.angle_gun = random.randint(-30, 30)
        self.angle_v = ANGLE_SPEED
        self.color = tank_color
        self.n_hits = 0
        self.cooldown = 0

    def draw(self, screen):
        GUN_LINE_WIDTH = 5
        TANK_LINE_WIDTH = 5

        # draw the tank
        pg.draw.rect(
            screen,
            self.color,
            pg.rect.Rect(self.px, self.py, self.w, self.h),
            TANK_LINE_WIDTH)

        # draw the gun
        (st_x, st_y), (end_x, end_y) = self.gun_position()
        pg.draw.line(
            screen,
            self.color,
            (st_x, st_y),
            (end_x, end_y),
            GUN_LINE_WIDTH
        )

    def gun_position(self):
        GUN_SIZE = 50
        dx, dy = self.gun_direction()
        dx *= GUN_SIZE
        dy *= GUN_SIZE
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
        ANGLE_LIMIT = 60

        # update the gun angle
        self.angle_gun += self.angle_v
        if abs(self.angle_gun) >= ANGLE_LIMIT:
            self.angle_v *= -1

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


def perform_shot(player: Tank, projectiles: List[Projectile]):
    _, (x, y) = player.gun_position()
    dir_x, dir_y = player.gun_direction()
    new_projectile = Projectile(
        x, y, player.color, Config.PROJECTILE_RADIUS)
    new_projectile.v_x = player.v_x + Config.PROJECTILE_SPEED * dir_x
    new_projectile.v_y = player.v_y + Config.PROJECTILE_SPEED * dir_y
    projectiles.append(new_projectile)


def update_game_objects(player_1, player_2, projectiles):
    player_1.update(
        Config.SCREEN_WIDTH,
        Config.FLOOR_HEIGHT,
        Config.GRAVITY
    )
    player_2.update(
        Config.SCREEN_WIDTH,
        Config.FLOOR_HEIGHT,
        Config.GRAVITY
    )

    for p in projectiles:
        p.update(
            Config.SCREEN_WIDTH,
            Config.FLOOR_HEIGHT,
            Config.GRAVITY
        )


def remove_projectiles_in_the_floor(projectiles):
    new_list = []

    for p in projectiles:
        if not is_in_the_floor(p):
            new_list.append(p)

    return new_list


def draw_objects(screen, player_1, player_2, projectiles, font):
    screen.fill((255, 255, 255))

    # draw the floor
    pg.draw.rect(
        screen,
        (153, 51, 0),
        pg.rect.Rect(0, Config.FLOOR_HEIGHT,
                     Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
    )

    # draw players
    player_1.draw(screen)
    player_2.draw(screen)

    # draw projectiles
    for p in projectiles:
        p.draw(screen)

    # draw score
    img = font.render(
        f'{player_2.n_hits} x {player_1.n_hits}', True, (0, 0, 0))

    screen.blit(img, (Config.SCREEN_WIDTH * 0.45, 20))

    pg.display.flip()


def circle_rectangle_collision_test(circle, rect):
    DeltaX = circle.px - max(rect.px, min(circle.px, rect.px + rect.w))
    DeltaY = circle.py - max(rect.py, min(circle.py, rect.py + rect.h))
    return (DeltaX * DeltaX + DeltaY * DeltaY) < (circle.r * circle.r)


def test_collisions(projectiles, player):
    projectiles_without_collision = []
    for p in projectiles:
        if circle_rectangle_collision_test(p, player):
            player.n_hits += 1
        else:
            projectiles_without_collision.append(p)
    projectiles[:] = projectiles_without_collision


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

    player_2 = Tank(
        int(Config.SCREEN_WIDTH * 0.9) - Config.TANK_WIDTH,
        TANK_INITIAL_Y,
        Config.TANK_HEIGHT,
        Config.TANK_WIDTH,
        (0, 0, 255)
    )

    projectiles = []

    font = pg.font.SysFont(None, 48)
    finish_game = False

    # main loop
    while not finish_game:
        update_game_objects(player_1, player_2, projectiles)
        projectiles = remove_projectiles_in_the_floor(projectiles)
        test_collisions(projectiles, player_1)
        test_collisions(projectiles, player_2)
        draw_objects(screen, player_1, player_2, projectiles, font)

        # event handling, gets all event from the event queue
        for event in pg.event.get():
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_a)) or (pg.key.get_pressed()[pg.K_a]):
                player_1.v_x = -Config.TANK_SPEED
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_d)) or (pg.key.get_pressed()[pg.K_d]):
                player_1.v_x = Config.TANK_SPEED
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_e)) or (pg.key.get_pressed()[pg.K_e]):
                perform_shot(player_1, projectiles)
            if (is_in_the_floor(player_1)) and (((event.type == pg.KEYDOWN) and (event.key == pg.K_w)) or (pg.key.get_pressed()[pg.K_w])):
                player_1.v_y = Config.JUMP_SPEED
            if ((event.type == pg.KEYUP) and (event.key == pg.K_a)) or \
                    ((event.type == pg.KEYUP) and (event.key == pg.K_d)):
                player_1.v_x = 0

            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_j)) or (pg.key.get_pressed()[pg.K_j]):
                player_2.v_x = -Config.TANK_SPEED
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_l)) or (pg.key.get_pressed()[pg.K_l]):
                player_2.v_x = Config.TANK_SPEED
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_u)) or (pg.key.get_pressed()[pg.K_u]):
                perform_shot(player_2, projectiles)
            if (is_in_the_floor(player_2)) and (((event.type == pg.KEYDOWN) and (event.key == pg.K_i)) or (pg.key.get_pressed()[pg.K_i])):
                player_2.v_y = Config.JUMP_SPEED
            if ((event.type == pg.KEYUP) and (event.key == pg.K_j)) or \
                    ((event.type == pg.KEYUP) and (event.key == pg.K_l)):
                player_2.v_x = 0

                # only do something if the event is of type QUIT
            if (event.type == pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                finish_game = True


if __name__ == "__main__":
    main()
