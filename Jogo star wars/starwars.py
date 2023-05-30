import pygame
import random
import ctypes

ctypes.windll.user32.SetProcessDPIAware()

# Iniciando o Pygame
pygame.init() 

# Definindo as dimensões da tela    
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

# Esconder o cursor
pygame.mouse.set_visible(False)

# Definindo as cores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Definindo a fonte do texto
FONT1 = pygame.font.Font(None, 40)
FONT2 = pygame.font.Font(None, 80)

# Definindo a taxa de atualização do jogo (em FPS)
FPS = 60

# Definindo a variável de pontuação do jogo
SCORE = 0

# Carregando as imagens
PLAYER_IMAGE = pygame.image.load("imagens/player.png").convert_alpha()
ENEMY_IMAGE = pygame.image.load("imagens/enemy.png").convert_alpha()
OBSTACLE_IMAGE_1 = pygame.image.load("imagens/obstacle1.png").convert_alpha()
POWER_UP_IMAGE = pygame.image.load("imagens/powerup.png").convert_alpha()
BONUS_IMAGE = pygame.image.load("imagens/bonus.png").convert_alpha()
START_BACKGROUND_IMAGE = pygame.image.load("imagens/start.jpg").convert_alpha()
BACKGROUND_IMAGE = pygame.image.load("imagens/background.jpg").convert_alpha()
GAME_OVER_IMAGE = pygame.image.load("imagens/gameover.jpg").convert_alpha()

# Redimensionando as imagens
PLAYER_IMAGE = pygame.transform.scale(PLAYER_IMAGE, (70, 85))
ENEMY_IMAGE = pygame.transform.scale(ENEMY_IMAGE, (70, 70))
OBSTACLE_IMAGE_1 = pygame.transform.scale(OBSTACLE_IMAGE_1, (100, 100))
POWER_UP_IMAGE = pygame.transform.scale(POWER_UP_IMAGE, (30, 30))
BONUS_IMAGE = pygame.transform.scale(BONUS_IMAGE, (30, 30))
START_BACKGROUND_IMAGE = pygame.transform.scale(START_BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
GAME_OVER_IMAGE = pygame.transform.scale(GAME_OVER_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Carregando os sons
PEW_SOUND = pygame.mixer.Sound("sons/pew.wav")
EXPLOSION_SOUND = pygame.mixer.Sound("sons/explosion.wav")
EXPLOSION_SOUND.set_volume(0.3)
START_MUSIC = pygame.mixer.Sound("sons/startmusic.wav")
START_MUSIC.set_volume(0.5)
END_MUSIC = pygame.mixer.Sound("sons/endmusic.wav")
END_MUSIC.set_volume(0.6)

# Velocidade do tiro
bullets_speed = 10

# Define a posição inicial do cursor
pygame.mouse.set_pos(760, 750)

# Definindo as funções do jogo
def draw_text1(text, color, x, y):
    text_surface = FONT1.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_text2(text, color, x, y):
    text_surface = FONT2.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def update_enemies():
    for enemy in enemies:
        enemy.bottom += 8
        if enemy.top > SCREEN_HEIGHT:
            enemy.left = random.randint(0, SCREEN_WIDTH - enemy.width)
            enemy.bottom = random.randint(-1000, -100)

def update_obstacles():
    for obstacle in obstacles:
        obstacle.top += 6
        if obstacle.top > SCREEN_HEIGHT:
            obstacles.remove(obstacle)
            obstacle_rect = OBSTACLE_IMAGE_1.get_rect()
            obstacle_rect.left = random.randint(0, SCREEN_WIDTH - obstacle_rect.width)
            obstacle_rect.bottom = 0
            obstacles.append(obstacle_rect)

def update_powerup():
    for powerup in powerups:
        powerup.top += 2
        if powerup.top > SCREEN_HEIGHT:
            powerups.remove(powerup)
            power_up_rect = POWER_UP_IMAGE.get_rect()
            power_up_rect.left = random.randint(0, SCREEN_WIDTH - power_up_rect.width)
            power_up_rect.bottom = 0
            powerups.append(power_up_rect)

def update_bonus():
    for bonus in bonuss:
        bonus.top += 1
        if bonus.top > SCREEN_HEIGHT:
            bonuss.remove(bonus)
            bonus_rect = BONUS_IMAGE.get_rect()
            bonus_rect.left = random.randint(0, SCREEN_WIDTH - bonus_rect.width)
            bonus_rect.bottom = 0
            bonuss.append(bonus_rect)

def check_collision():
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            EXPLOSION_SOUND.play()
            return True
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            EXPLOSION_SOUND.play()
            return True
    return False

def show_game_over_screen():
    END_MUSIC.play()
    screen.fill(BLACK)
    screen.blit(GAME_OVER_IMAGE, (0, 0))
    draw_text2("Game Over", RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text1("Pressione start para voltar ao menu", YELLOW, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
    pontuação_final = FONT1.render("Sua pontuação final foi: " + str(SCORE), True, WHITE)
    screen.blit(pontuação_final, (SCREEN_WIDTH/2 - pontuação_final.get_width()/2, SCREEN_HEIGHT/2 - pontuação_final.get_height()/2 + 120))
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    END_MUSIC.stop()
                    show_start_screen()

def show_end_game_screen():
    START_MUSIC.play()
    screen.fill(BLACK)
    draw_text2("Parabéns, a força está com você!", YELLOW, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text1("Pressione start para continuar", WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    START_MUSIC.stop()
                    waiting = False
                    show_start_screen()

def show_start_screen():
    global SCORE
    SCORE = 0
    screen.fill(BLACK)
    screen.blit(START_BACKGROUND_IMAGE, (0, 0))
    draw_text1("Alcance uma pontuação de 60.000 para desbloquear o final do jogo!", YELLOW, SCREEN_WIDTH // 2 - 270, SCREEN_HEIGHT // 2 - 360)
    draw_text2("Star Wars", YELLOW, SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT // 2 - 300)
    draw_text1("Pressione start para começar", YELLOW, SCREEN_WIDTH // 2 - 515, SCREEN_HEIGHT // 2 - 240)
    START_MUSIC.play()
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

# Criando a tela do jogo
screen.blit(BACKGROUND_IMAGE, (0, 0))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Star Wars")

# Exibindo a tela de início
show_start_screen()

# Inicializando o jogo
clock = pygame.time.Clock()
player_rect = PLAYER_IMAGE.get_rect()
player_rect.centerx = SCREEN_WIDTH // 2
player_rect.bottom = SCREEN_HEIGHT - 10
players = []
enemies = []
for i in range(5):
    enemy_rect = ENEMY_IMAGE.get_rect()
    enemy_rect.left = random.randint(0, SCREEN_WIDTH - enemy_rect.width)
    enemy_rect.bottom = random.randint(-1000, -100)

# Inicialização dos bonus
bonuss = []

# Inicialização dos obstáculos
obstacles = []

# Inicialização dos power ups
powerups = []

# Inicialização da lista de tiros
bullets = []

# Adicionando os inimigos à lista
enemies.append(enemy_rect)

# Adicionando o player à lista
players.append(player_rect)

# Defina o relógio do jogo
clock = pygame.time.Clock()

# Loop principal do jogo
running = True
game_over = False
end_game = False
while running:
    START_MUSIC.stop()
    END_MUSIC.stop()
    if end_game:
        show_end_game_screen()
        end_game = False
        player_rect.centerx = SCREEN_WIDTH // 2
        player_rect.bottom = SCREEN_HEIGHT - 10
        enemies = []
        for i in range(5):
            enemy_rect = ENEMY_IMAGE.get_rect()
            enemy_rect.left = random.randint(0, SCREEN_WIDTH - enemy_rect.width)
            enemy_rect.bottom = random.randint(-1000, -100)
            enemies.append(enemy_rect)
        obstacles = []
        for j in range(5):
            obstacle_rect = OBSTACLE_IMAGE_1.get_rect()
            obstacle_rect.left = random.randint(0, SCREEN_WIDTH - obstacle_rect.width)
            obstacle_rect.bottom = random.randint(-1000, -100)
            obstacles.append(obstacle_rect)
        bonuss = []
        for k in range(1):
            bonus_rect = BONUS_IMAGE.get_rect()
            bonus_rect.left = random.randint(0, SCREEN_WIDTH - bonus_rect.width)
            bonus_rect.bottom = random.randint(-1000, -100)
            bonuss.append(bonus_rect)
        powerups = []
        for l in range(1):
            power_up_rect = POWER_UP_IMAGE.get_rect()
            power_up_rect.left = random.randint(0, SCREEN_WIDTH - power_up_rect.width)
            power_up_rect.bottom = random.randint(-1000, -100)
            powerups.append(power_up_rect)
    if game_over:
        show_game_over_screen()
        game_over = False
        player_rect.centerx = SCREEN_WIDTH // 2
        player_rect.bottom = SCREEN_HEIGHT - 10
        enemies = []
        for i in range(5):
            enemy_rect = ENEMY_IMAGE.get_rect()
            enemy_rect.left = random.randint(0, SCREEN_WIDTH - enemy_rect.width)
            enemy_rect.bottom = random.randint(-1000, -100)
            enemies.append(enemy_rect)
        obstacles = []
        for j in range(5):
            obstacle_rect = OBSTACLE_IMAGE_1.get_rect()
            obstacle_rect.left = random.randint(0, SCREEN_WIDTH - obstacle_rect.width)
            obstacle_rect.bottom = random.randint(-1000, -100)
            obstacles.append(obstacle_rect)
        bonuss = []
        for k in range(1):
            bonus_rect = BONUS_IMAGE.get_rect()
            bonus_rect.left = random.randint(0, SCREEN_WIDTH - bonus_rect.width)
            bonus_rect.bottom = random.randint(-1000, -100)
            bonuss.append(bonus_rect)
        powerups = []
        for l in range(1):
            power_up_rect = POWER_UP_IMAGE.get_rect()
            power_up_rect.left = random.randint(0, SCREEN_WIDTH - power_up_rect.width)
            power_up_rect.bottom = random.randint(-1000, -100)
            powerups.append(power_up_rect)
    else:
        # Atualização dos objetos do jogo
        update_enemies()
        update_obstacles()
        update_powerup()
        update_bonus()
        # Eventos do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    PEW_SOUND.play()
                    bullet_rect = pygame.Rect(player_rect.centerx - 5, player_rect.top - 10, 5, 30)
                    bullets.append(bullet_rect)

        player_position = pygame.mouse.get_pos()
        player_rect.centerx = player_position[0]
        
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > SCREEN_WIDTH:
            player_rect.right = SCREEN_WIDTH
        for bullet in bullets:
            bullet.top -= bullets_speed
            if bullet.bottom < 0:
                bullets.remove(bullet)
            else:
                for enemy in enemies:
                    if bullet.colliderect(enemy):
                        EXPLOSION_SOUND.play()
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        SCORE += 30
                for obstacle in obstacles:
                    if bullet.colliderect(obstacle):
                        EXPLOSION_SOUND.play()
                        bullets.remove(bullet)
                        obstacles.remove(obstacle)
                        SCORE += 10
        for powerup in powerups:
            if player_rect.colliderect(powerup):
                powerups.remove(powerup)
                EXPLOSION_SOUND.play()
                for enemy in enemies:
                    enemies.clear()
                    SCORE += 100
                for obstacle in obstacles:
                    obstacles.clear()
                    SCORE += 25
        for bonus in bonuss:
            if player_rect.colliderect(bonus):
                SCORE += 500
                bonuss.remove(bonus)

        if len(enemies) < 5:
            enemy_rect = ENEMY_IMAGE.get_rect()
            enemy_rect.left = random.randint(0, SCREEN_WIDTH - enemy_rect.width)
            enemy_rect.bottom = random.randint(-1000, -100)
            enemies.append(enemy_rect)
        if len(obstacles) < 3:
            obstacle_rect = OBSTACLE_IMAGE_1.get_rect()
            obstacle_rect.left = random.randint(0, SCREEN_WIDTH - obstacle_rect.width)
            obstacle_rect.bottom = 0
            obstacles.append(obstacle_rect)
        if len(powerups) < 1:
            power_up_rect = POWER_UP_IMAGE.get_rect()
            power_up_rect.left = random.randint(0, SCREEN_WIDTH - power_up_rect.width)
            power_up_rect.bottom = 0
            powerups.append(power_up_rect)
        if len(bonuss) < 1:
            bonus_rect = BONUS_IMAGE.get_rect()
            bonus_rect.left = random.randint(0, SCREEN_WIDTH - bonus_rect.width)
            bonus_rect.bottom = 0
            bonuss.append(bonus_rect)

        if check_collision():
            game_over = True

        # Desenho dos objetos do jogo
        screen.fill(BLACK)
        screen.blit(BACKGROUND_IMAGE, (0, 0))
        for enemy in enemies:
            screen.blit(ENEMY_IMAGE, enemy)
        for obstacle in obstacles:
            screen.blit(OBSTACLE_IMAGE_1, obstacle)
        for bonus in bonuss:
            screen.blit(BONUS_IMAGE, bonus)
        for powerup in powerups:
            screen.blit(POWER_UP_IMAGE, powerup)
        for bullet in bullets:
            pygame.draw.rect(screen, RED, bullet)
        screen.blit(PLAYER_IMAGE, player_rect)
        # Desenhar a pontuação na tela
        TEXT = FONT1.render("Pontuação: " + str(SCORE), True, WHITE)
        screen.blit(TEXT, (10, 10))
        pygame.display.update()

        if SCORE >= 10000:
            for i in range(8):
                if len(enemies) < 8:
                    enemy_rect = ENEMY_IMAGE.get_rect()
                    enemy_rect.left = random.randint(0, SCREEN_WIDTH - enemy_rect.width)
                    enemy_rect.bottom = random.randint(-1000, -100)
                    enemies.append(enemy_rect)
        
        if SCORE >= 30000:
            for i in range(12):
                if len(enemies) < 12:
                    enemy_rect = ENEMY_IMAGE.get_rect()
                    enemy_rect.left = random.randint(0, SCREEN_WIDTH - enemy_rect.width)
                    enemy_rect.bottom = random.randint(-1000, -100)
                    enemies.append(enemy_rect)

        if SCORE >= 50000:
            for i in range(16):
                if len(enemies) < 16:
                    enemy_rect = ENEMY_IMAGE.get_rect()
                    enemy_rect.left = random.randint(0, SCREEN_WIDTH - enemy_rect.width)
                    enemy_rect.bottom = random.randint(-1000, -100)
                    enemies.append(enemy_rect)

        if SCORE >= 59000:
            for i in range(24):
                if len(enemies) < 24:
                    enemy_rect = ENEMY_IMAGE.get_rect()
                    enemy_rect.left = random.randint(0, SCREEN_WIDTH - enemy_rect.width)
                    enemy_rect.bottom = random.randint(-1000, -100)
                    enemies.append(enemy_rect)

        if SCORE >= 60000:
            end_game = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Atualização do relógio
        clock.tick(FPS)

# Finalizando o Pygame
pygame.quit()