import pygame
import sys
import random
pygame.init()
# WINDOW
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Swap Runner")
FPS = 60
clock = pygame.time.Clock()
# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (80, 160, 255)
RED = (255, 80, 80)
player_size = 40
player_x = 100
player_y = HEIGHT - player_size
gravity_down = True
gravity_speed = 8
# OBSTACLES
obstacles = []      # each item: [x, y, height]
obstacle_width = 40
base_obstacle_speed = 6
obstacle_speed = base_obstacle_speed
# SCORE
score = 0
def draw_player():
    pygame.draw.rect(WIN, BLUE, (player_x, player_y, player_size, player_size))
def draw_obstacles():
    for ox, oy, oh in obstacles:
        pygame.draw.rect(WIN, RED, (ox, oy, obstacle_width, oh))
def game_over_screen(final_score):
    font = pygame.font.SysFont("Arial", 55, True)
    small = pygame.font.SysFont("Arial", 28, True)
    while True:
        WIN.fill(BLACK)
        text = font.render("GAME OVER", True, RED)
        scr = small.render(f"Score : {final_score}", True, WHITE)
        msg = small.render("Press SPACE to Restart", True, WHITE)
        WIN.blit(text, (WIDTH/2 - text.get_width()/2, 120))
        WIN.blit(scr, (WIDTH/2 - scr.get_width()/2, 200))
        WIN.blit(msg, (WIDTH/2 - msg.get_width()/2, 260))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                main_game()
                return
        pygame.display.update()
        clock.tick(FPS)
def main_game():
    global player_y, gravity_down, obstacles, score, obstacle_speed
    player_y = HEIGHT - player_size
    gravity_down = True
    obstacles = []
    score = 0
    obstacle_speed = base_obstacle_speed
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gravity_down = not gravity_down  # Only SPACE changes gravity
        if gravity_down:
            player_y += gravity_speed
        else:
            player_y -= gravity_speed
        if player_y < 0:
            player_y = 0
        if player_y + player_size > HEIGHT:
            player_y = HEIGHT - player_size
        # SPAWN OBSTACLES (random heights)
        if len(obstacles) == 0 or obstacles[-1][0] < WIDTH - random.randint(150, 300):

            pattern = random.randint(1, 4)

            # Random height for obstacle
            h1 = random.randint(20, 120)

            if pattern == 1:  # Single Top
                obstacles.append([WIDTH, 0, h1])

            if pattern == 2:  # Single Bottom
                obstacles.append([WIDTH, HEIGHT - h1, h1])

            if pattern == 3:  # Double (Top + Bottom)
                h2 = random.randint(20, 120)
                obstacles.append([WIDTH, 0, h1])
                obstacles.append([WIDTH + 60, HEIGHT - h2, h2])

            if pattern == 4:  # Double same side
                side = random.choice(["top", "bottom"])
                h2 = random.randint(20, 120)

                if side == "top":
                    obstacles.append([WIDTH, 0, h1])
                    obstacles.append([WIDTH + 80, 0, h2])
                else:
                    obstacles.append([WIDTH, HEIGHT - h1, h1])
                    obstacles.append([WIDTH + 80, HEIGHT - h2, h2])
        for i in range(len(obstacles)):
            obstacles[i][0] -= obstacle_speed
        obstacles = [o for o in obstacles if o[0] > -obstacle_width]
        for ox, oy, oh in obstacles:
            if (
                player_x < ox + obstacle_width and
                player_x + player_size > ox and
                player_y < oy + oh and
                player_y + player_size > oy
            ):
                game_over_screen(score)
                return
        score +=1

        if score % 100 == 0:
            obstacle_speed += 0.5
        # DRAW EVERYTHING
        WIN.fill(BLACK)
        draw_player()
        draw_obstacles()

        font = pygame.font.SysFont("Arial", 28, True)
        s = font.render(f"Score: {score}", True, WHITE)
        WIN.blit(s, (10, 10))

        pygame.display.update()
def start_screen():
    title_font = pygame.font.SysFont("Arial", 60, True)
    info_font = pygame.font.SysFont("Arial", 28, True)

    while True:
        WIN.fill(BLACK)

        title = title_font.render("UPSIDE DOWN RUNNER", True, BLUE)
        info1 = info_font.render("Press SPACE to Start", True, WHITE)
        info2 = info_font.render("Press SPACE during game to flip gravity", True, WHITE)

        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 120))
        WIN.blit(info1, (WIDTH//2 - info1.get_width()//2, 220))
        WIN.blit(info2, (WIDTH//2 - info2.get_width()//2, 260))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # Exit start screen → go to game

        pygame.display.update()
        clock.tick(FPS)
start_screen()
main_game()
