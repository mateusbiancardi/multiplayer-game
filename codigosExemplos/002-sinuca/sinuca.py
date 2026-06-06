
import math
import random
import pygame as pg


def main():
    pg.init()

    # create a surface on screen that has the size of 700 x 200
    screen = pg.display.set_mode((900, 400))

    arena = pg.rect.Rect(10, 10, 880, 380)

    ball_pos_x = 450
    ball_pos_y = 200

    v_x = 0
    v_y = 0

    hit_mode = True

    resist = 0.9995

    cacapa1_x = 10
    cacapa1_y = 10
    cacapa2_x = 440
    cacapa2_y = 10
    cacapa3_x = 440
    cacapa3_y = 390
    cacapa4_x = 890
    cacapa4_y = 10
    cacapa5_x = 10
    cacapa5_y = 390
    cacapa6_x = 890
    cacapa6_y = 390

    font = pg.font.SysFont(None, 48)

    points = 0

    finish_game = False

    # main loop
    while not finish_game:
        screen.fill((255, 255, 255))
        pg.draw.rect(screen, (0, 128, 0), arena)
        pg.draw.circle(screen, (255, 255, 255), (ball_pos_x, ball_pos_y), 10)
        pg.draw.circle(screen, (0, 0, 0), (cacapa1_x, cacapa1_y), 20)
        pg.draw.circle(screen, (0, 0, 0), (cacapa2_x, cacapa2_y), 20)
        pg.draw.circle(screen, (0, 0, 0), (cacapa3_x, cacapa3_y), 20)
        pg.draw.circle(screen, (0, 0, 0), (cacapa4_x, cacapa4_y), 20)
        pg.draw.circle(screen, (0, 0, 0), (cacapa5_x, cacapa5_y), 20)
        pg.draw.circle(screen, (0, 0, 0), (cacapa6_x, cacapa6_y), 20)

        img = font.render(f'{points}', True, (255, 255, 255))
        screen.blit(img, (200, 20))

        mouse_pos = pg.mouse.get_pos()
        d = math.sqrt(
            (ball_pos_y - mouse_pos[1]) ** 2 +
            (ball_pos_x - mouse_pos[0]) ** 2
        )

        std = 2 + math.exp(d * 0.04)

        mouse_pos = (
            mouse_pos[0] + random.normalvariate(0, std),
            mouse_pos[1] + random.normalvariate(0, std),
        )

        a = math.atan2(
            ball_pos_y - mouse_pos[1],
            ball_pos_x - mouse_pos[0])
        dx = ball_pos_x - 25 * math.cos(a)
        dy = ball_pos_y - 25 * math.sin(a)

        if hit_mode:
            pg.draw.line(screen, (255, 0, 0), (dx, dy),
                         (ball_pos_x, ball_pos_y), 4)

        pg.display.flip()

        ball_pos_x += v_x
        ball_pos_y += v_y

        v_x *= resist
        v_y *= resist

        if abs(v_x) <= 0.02:
            v_x = 0

        if abs(v_y) <= 0.02:
            v_y = 0

        if abs(v_x) == 0.0 and abs(v_y) == 0.0:
            hit_mode = True

        if (ball_pos_y >= 390) or (ball_pos_y <= 10):
            v_y = -v_y

        if (ball_pos_x >= 890) or (ball_pos_x <= 10):
            v_x = -v_x

        hole_hit = False

        # collision with hole 1
        if math.sqrt((ball_pos_y - cacapa1_y) ** 2 + (ball_pos_x - cacapa1_x) ** 2) < 20:
            hole_hit = True
        if math.sqrt((ball_pos_y - cacapa2_y) ** 2 + (ball_pos_x - cacapa2_x) ** 2) < 20:
            hole_hit = True
        if math.sqrt((ball_pos_y - cacapa3_y) ** 2 + (ball_pos_x - cacapa3_x) ** 2) < 20:
            hole_hit = True
        if math.sqrt((ball_pos_y - cacapa4_y) ** 2 + (ball_pos_x - cacapa3_x) ** 2) < 20:
            hole_hit = True
        if math.sqrt((ball_pos_y - cacapa5_y) ** 2 + (ball_pos_x - cacapa5_x) ** 2) < 20:
            hole_hit = True
        if math.sqrt((ball_pos_y - cacapa6_y) ** 2 + (ball_pos_x - cacapa6_x) ** 2) < 20:
            hole_hit = True

        if hole_hit:
            points += 1
            ball_pos_x = random.randint(10, 890)
            ball_pos_y = random.randint(10, 390)
            hole_hit = False
            v_x = 0
            v_y = 0

            # event handling, gets all event from the event queue
        for event in pg.event.get():
            if hit_mode and (event.type == pg.MOUSEBUTTONDOWN):
                v_x = -0.75 * math.cos(a)
                v_y = -0.75 * math.sin(a)
                hit_mode = False

            # only do something if the event is of type QUIT
            if (event.type == pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                finish_game = True

    pg.quit()


if __name__ == "__main__":
    main()
