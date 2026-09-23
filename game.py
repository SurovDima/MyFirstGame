import pygame
import random
import math

pygame.init()

# ==================================================
# НАСТРОЙКИ
# ==================================================

WIDTH = 900
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEON DRIVE")

clock = pygame.time.Clock()

# ==================================================
# ЦВЕТА
# ==================================================

BLACK = (3, 5, 15)
WHITE = (245, 248, 255)

BLUE = (0, 210, 255)
CYAN = (0, 255, 240)

PURPLE = (150, 60, 255)
PINK = (255, 40, 180)

RED = (255, 40, 50)
ORANGE = (255, 120, 20)
YELLOW = (255, 220, 50)

GREEN = (50, 255, 160)
GRAY = (110, 120, 145)

# ==================================================
# ШРИФТЫ
# ==================================================

title_font = pygame.font.Font(None, 90)
big_font = pygame.font.Font(None, 75)
font = pygame.font.Font(None, 38)
small_font = pygame.font.Font(None, 25)

# ==================================================
# СОСТОЯНИЕ
# ==================================================

game_state = "menu"

nickname = ""

score = 0
best_score = 0

player_speed = 7
fire_speed = 4

# ==================================================
# МАШИНА
# ==================================================

car = pygame.Rect(
    WIDTH // 2 - 30,
    HEIGHT - 110,
    60,
    90
)

# ==================================================
# ОГОНЬ
# ==================================================

fires = []

for i in range(6):

    fire = pygame.Rect(
        random.randint(30, WIDTH - 70),
        random.randint(-1000, -50),
        45,
        55
    )

    fires.append(fire)

# ==================================================
# ЧАСТИЦЫ ФОНА
# ==================================================

particles = []

for i in range(120):

    particles.append({
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "speed": random.uniform(0.3, 1.5),
        "size": random.randint(1, 3)
    })

# ==================================================
# ГОРОД
# ==================================================

buildings = []

x = 0

while x < WIDTH:

    width = random.randint(45, 90)
    height = random.randint(100, 250)

    buildings.append({
        "x": x,
        "width": width,
        "height": height
    })

    x += width + random.randint(5, 15)

# ==================================================
# ФОН
# ==================================================

background = pygame.Surface(
    (WIDTH, HEIGHT)
)

for y in range(HEIGHT):

    progress = y / HEIGHT

    r = int(3 + progress * 7)
    g = int(5 + progress * 8)
    b = int(18 + progress * 25)

    pygame.draw.line(
        background,
        (r, g, b),
        (0, y),
        (WIDTH, y)
    )

# ==================================================
# ЧАСТИЦЫ
# ==================================================

def update_particles():

    for particle in particles:

        particle["y"] += particle["speed"]

        if particle["y"] > HEIGHT:

            particle["y"] = 0
            particle["x"] = random.randint(0, WIDTH)


def draw_particles():

    for particle in particles:

        pygame.draw.circle(
            screen,
            (70, 90, 150),
            (
                int(particle["x"]),
                int(particle["y"])
            ),
            particle["size"]
        )

# ==================================================
# СВЕЧЕНИЕ
# ==================================================

def draw_glow(x, y, radius, color):

    glow = pygame.Surface(
        (radius * 4, radius * 4),
        pygame.SRCALPHA
    )

    center = radius * 2

    for size in range(radius * 2, 0, -5):

        alpha = int(
            60 * (size / (radius * 2))
        )

        pygame.draw.circle(
            glow,
            (*color, alpha),
            (center, center),
            size
        )

    screen.blit(
        glow,
        (
            x - center,
            y - center
        )
    )

# ==================================================
# ГОРОД
# ==================================================

def draw_city():

    for building in buildings:

        x = building["x"]
        width = building["width"]
        height = building["height"]

        y = HEIGHT - height

        # здание

        pygame.draw.rect(
            screen,
            (7, 10, 25),
            (
                x,
                y,
                width,
                height
            )
        )

        # контур

        pygame.draw.rect(
            screen,
            (20, 30, 65),
            (
                x,
                y,
                width,
                height
            ),
            1
        )

        # окна

        window_y = y + 15

        while window_y < HEIGHT - 20:

            window_x = x + 10

            while window_x < x + width - 10:

                if random.random() > 0.3:

                    color = random.choice([
                        BLUE,
                        PURPLE,
                        PINK
                    ])

                    pygame.draw.rect(
                        screen,
                        color,
                        (
                            window_x,
                            window_y,
                            5,
                            8
                        )
                    )

                window_x += 15

            window_y += 20

# ==================================================
# НЕОНОВАЯ ДОРОГА
# ==================================================

def draw_road():

    road_top = 400

    # дорога

    pygame.draw.polygon(
        screen,
        (8, 10, 22),
        [
            (WIDTH // 2 - 180, road_top),
            (WIDTH // 2 + 180, road_top),
            (WIDTH, HEIGHT),
            (0, HEIGHT)
        ]
    )

    # левая линия

    pygame.draw.line(
        screen,
        PURPLE,
        (WIDTH // 2 - 180, road_top),
        (0, HEIGHT),
        3
    )

    # правая линия

    pygame.draw.line(
        screen,
        BLUE,
        (WIDTH // 2 + 180, road_top),
        (WIDTH, HEIGHT),
        3
    )

    # центральная разметка

    pygame.draw.line(
        screen,
        (30, 40, 70),
        (WIDTH // 2, road_top),
        (WIDTH // 2, HEIGHT),
        2
    )

# ==================================================
# МАШИНА
# ==================================================

def draw_car():

    x = car.centerx
    y = car.centery

    # голубое свечение

    draw_glow(
        x,
        y,
        65,
        BLUE
    )

    # колёса

    pygame.draw.rect(
        screen,
        (5, 5, 10),
        (
            x - 36,
            y - 30,
            12,
            28
        ),
        border_radius=5
    )

    pygame.draw.rect(
        screen,
        (5, 5, 10),
        (
            x + 24,
            y - 30,
            12,
            28
        ),
        border_radius=5
    )

    pygame.draw.rect(
        screen,
        (5, 5, 10),
        (
            x - 36,
            y + 15,
            12,
            28
        ),
        border_radius=5
    )

    pygame.draw.rect(
        screen,
        (5, 5, 10),
        (
            x + 24,
            y + 15,
            12,
            28
        ),
        border_radius=5
    )

    # корпус

    pygame.draw.rect(
        screen,
        BLUE,
        (
            x - 27,
            y - 45,
            54,
            90
        ),
        border_radius=16
    )

    # крыша

    pygame.draw.polygon(
        screen,
        (30, 120, 180),
        [
            (x - 20, y - 15),
            (x - 15, y - 35),
            (x + 15, y - 35),
            (x + 20, y - 15)
        ]
    )

    # стекло

    pygame.draw.polygon(
        screen,
        (10, 25, 45),
        [
            (x - 14, y - 15),
            (x - 10, y - 30),
            (x + 10, y - 30),
            (x + 14, y - 15)
        ]
    )

    # фары

    pygame.draw.circle(
        screen,
        WHITE,
        (x - 16, y - 37),
        5
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (x + 16, y - 37),
        5
    )

    # задние огни

    pygame.draw.rect(
        screen,
        RED,
        (
            x - 18,
            y + 32,
            12,
            5
        ),
        border_radius=2
    )

    pygame.draw.rect(
        screen,
        RED,
        (
            x + 6,
            y + 32,
            12,
            5
        ),
        border_radius=2
    )

# ==================================================
# ОГОНЬ
# ==================================================

def draw_fire(fire):

    x = fire.centerx
    y = fire.centery

    # большое свечение

    draw_glow(
        x,
        y,
        55,
        ORANGE
    )

    # внешнее пламя

    pygame.draw.polygon(
        screen,
        RED,
        [
            (x, y + 28),
            (x - 22, y + 5),
            (x - 15, y - 15),
            (x - 5, y - 2),
            (x, y - 28),
            (x + 10, y - 5),
            (x + 20, y - 15),
            (x + 18, y + 8)
        ]
    )

    # оранжевое пламя

    pygame.draw.polygon(
        screen,
        ORANGE,
        [
            (x, y + 20),
            (x - 14, y + 5),
            (x - 8, y - 10),
            (x, y),
            (x + 8, y - 13),
            (x + 13, y + 5)
        ]
    )

    # жёлтая середина

    pygame.draw.polygon(
        screen,
        YELLOW,
        [
            (x, y + 12),
            (x - 7, y),
            (x, y - 9),
            (x + 7, y)
        ]
    )

# ==================================================
# СБРОС ИГРЫ
# ==================================================

def reset_game():

    global score
    global fire_speed
    global game_state

    score = 0
    fire_speed = 4

    car.x = WIDTH // 2 - 30
    car.y = HEIGHT - 110

    for fire in fires:

        fire.x = random.randint(
            30,
            WIDTH - 70
        )

        fire.y = random.randint(
            -1000,
            -50
        )

    game_state = "game"

# ==================================================
# МЕНЮ
# ==================================================

def draw_menu():

    screen.blit(
        background,
        (0, 0)
    )

    draw_particles()
    draw_city()
    draw_road()

    # название

    title = title_font.render(
        "NEON DRIVE",
        True,
        WHITE
    )

    screen.blit(
        title,
        (
            WIDTH // 2 -
            title.get_width() // 2,
            80
        )
    )

    subtitle = small_font.render(
        "SURVIVE THE FIRE",
        True,
        ORANGE
    )

    screen.blit(
        subtitle,
        (
            WIDTH // 2 -
            subtitle.get_width() // 2,
            170
        )
    )

    # ==================================================
    # НИК
    # ==================================================

    box_width = 450
    box_height = 85

    box_x = WIDTH // 2 - box_width // 2
    box_y = 280

    pygame.draw.rect(
        screen,
        (10, 15, 35),
        (
            box_x,
            box_y,
            box_width,
            box_height
        ),
        border_radius=15
    )

    pygame.draw.rect(
        screen,
        BLUE,
        (
            box_x,
            box_y,
            box_width,
            box_height
        ),
        2,
        border_radius=15
    )

    if nickname == "":

        nick_text = small_font.render(
            "ENTER YOUR NICKNAME...",
            True,
            GRAY
        )

    else:

        nick_text = font.render(
            nickname,
            True,
            WHITE
        )

    screen.blit(
        nick_text,
        (
            WIDTH // 2 -
            nick_text.get_width() // 2,
            box_y + 25
        )
    )

    # курсор

    if pygame.time.get_ticks() % 1000 < 500:

        cursor_x = (
            WIDTH // 2 +
            nick_text.get_width() // 2 +
            5
        )

        pygame.draw.rect(
            screen,
            BLUE,
            (
                cursor_x,
                box_y + 22,
                3,
                35
            )
        )

    # START

    start_text = font.render(
        "PRESS ENTER TO START",
        True,
        GREEN
    )

    screen.blit(
        start_text,
        (
            WIDTH // 2 -
            start_text.get_width() // 2,
            400
        )
    )

    # управление

    info = small_font.render(
        "A / D  OR  ARROWS  •  DRIVE",
        True,
        GRAY
    )

    screen.blit(
        info,
        (
            WIDTH // 2 -
            info.get_width() // 2,
            460
        )
    )

# ==================================================
# ИГРА
# ==================================================

def draw_game():

    screen.blit(
        background,
        (0, 0)
    )

    draw_particles()
    draw_city()
    draw_road()

    # верхняя панель

    panel = pygame.Surface(
        (WIDTH, 75),
        pygame.SRCALPHA
    )

    panel.fill(
        (3, 5, 15, 225)
    )

    screen.blit(
        panel,
        (0, 0)
    )

    # ник

    nick_text = font.render(
        nickname,
        True,
        WHITE
    )

    screen.blit(
        nick_text,
        (25, 20)
    )

    # score

    score_text = font.render(
        f"SCORE  {score}",
        True,
        CYAN
    )

    screen.blit(
        score_text,
        (
            WIDTH -
            score_text.get_width() -
            25,
            20
        )
    )

    # огонь

    for fire in fires:

        draw_fire(fire)

    # машина

    draw_car()

# ==================================================
# GAME OVER
# ==================================================

def draw_game_over():

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 10, 200)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    box_width = 520
    box_height = 340

    box_x = WIDTH // 2 - box_width // 2
    box_y = HEIGHT // 2 - box_height // 2

    pygame.draw.rect(
        screen,
        (10, 14, 30),
        (
            box_x,
            box_y,
            box_width,
            box_height
        ),
        border_radius=20
    )

    pygame.draw.rect(
        screen,
        RED,
        (
            box_x,
            box_y,
            box_width,
            box_height
        ),
        2,
        border_radius=20
    )

    # GAME OVER

    text = big_font.render(
        "GAME OVER",
        True,
        RED
    )

    screen.blit(
        text,
        (
            WIDTH // 2 -
            text.get_width() // 2,
            box_y + 40
        )
    )

    # ник

    player_name = font.render(
        nickname,
        True,
        WHITE
    )

    screen.blit(
        player_name,
        (
            WIDTH // 2 -
            player_name.get_width() // 2,
            box_y + 125
        )
    )

    # score

    score_text = font.render(
        f"SCORE: {score}",
        True,
        CYAN
    )

    screen.blit(
        score_text,
        (
            WIDTH // 2 -
            score_text.get_width() // 2,
            box_y + 170
        )
    )

    # best

    best_text = small_font.render(
        f"BEST: {best_score}",
        True,
        GRAY
    )

    screen.blit(
        best_text,
        (
            WIDTH // 2 -
            best_text.get_width() // 2,
            box_y + 215
        )
    )

    # управление

    restart_text = small_font.render(
        "R  •  RESTART",
        True,
        GREEN
    )

    menu_text = small_font.render(
        "N  •  MENU",
        True,
        PURPLE
    )

    screen.blit(
        restart_text,
        (
            box_x + 90,
            box_y + 275
        )
    )

    screen.blit(
        menu_text,
        (
            box_x + 330,
            box_y + 275
        )
    )

# ==================================================
# ГЛАВНЫЙ ЦИКЛ
# ==================================================

running = True

while running:

    # ==================================================
    # СОБЫТИЯ
    # ==================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # ==================================================
        # МЕНЮ
        # ==================================================

        if game_state == "menu":

            if event.type == pygame.KEYDOWN:

                # ESC

                if event.key == pygame.K_ESCAPE:

                    running = False

                # BACKSPACE

                elif event.key == pygame.K_BACKSPACE:

                    nickname = nickname[:-1]

                # ENTER

                elif event.key == pygame.K_RETURN:

                    if nickname.strip() != "":

                        reset_game()

                # Ввод ника

                elif event.unicode.isprintable():

                    if len(nickname) < 14:

                        nickname += event.unicode

        # ==================================================
        # GAME OVER
        # ==================================================

        elif game_state == "game_over":

            if event.type == pygame.KEYDOWN:

                # R

                if event.key == pygame.K_r:

                    reset_game()

                # N

                elif event.key == pygame.K_n:

                    game_state = "menu"

                # ESC

                elif event.key == pygame.K_ESCAPE:

                    running = False

    # ==================================================
    # ЧАСТИЦЫ
    # ==================================================

    update_particles()

    # ==================================================
    # ИГРА
    # ==================================================

    if game_state == "game":

        keys = pygame.key.get_pressed()

        # влево

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:

            car.x -= player_speed

        # вправо

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:

            car.x += player_speed

        # границы

        if car.left < 0:

            car.left = 0

        if car.right > WIDTH:

            car.right = WIDTH

        # ==================================================
        # ОГОНЬ ДВИЖЕТСЯ
        # ==================================================

        for fire in fires:

            fire.y += fire_speed

            # огонь прошёл экран

            if fire.top > HEIGHT:

                fire.y = random.randint(
                    -700,
                    -50
                )

                fire.x = random.randint(
                    30,
                    WIDTH - 70
                )

                score += 1

            # столкновение

            if car.colliderect(fire):

                game_state = "game_over"

                if score > best_score:

                    best_score = score

        # ==================================================
        # СЛОЖНОСТЬ
        # ==================================================

        fire_speed = 4 + score // 10

    # ==================================================
    # ОТРИСОВКА
    # ==================================================

    if game_state == "menu":

        draw_menu()

    elif game_state == "game":

        draw_game()

    elif game_state == "game_over":

        draw_game()

        draw_game_over()

    # ==================================================
    # ОБНОВЛЕНИЕ
    # ==================================================

    pygame.display.flip()

    clock.tick(60)


pygame.quit()