import pygame
import random

# --- Настройки ---
WIDTH, HEIGHT = 1920, 1080
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RADIUS = 20
GAP = 15
FONT_NAME = "arial"
FPS = 60

WORDS = ["ЛИНЕЙКА", "ЗАРЯДНИК", "РЕАЛЬНОСТЬ", "ВСЕЛЕННАЯ", "ТЕРМОС", "ДЕМПФЕР", "РЕЗОНАТОР","ЭКСТРАСЕНС", "НАКАЛИВАНИЕ", "ХАМБАКЕ"]
WORDS = ["ДОЛЛАР", "ЗЕНИТ", "НОМИНАЦИЯ", "НАЦИОНАЛИЗМ", "ФАШИЗМ", "ДЕМПФЕР", "ДЕТОНАТОР","УЛЬТРАЗВУК", "ДЕФИЦИТ", "ЗЕЛЬЕВАРЕНИЕ"]

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Виселица")
clock = pygame.time.Clock()

def draw_text(text, size, color, x, y, center=True):
    font = pygame.font.SysFont(FONT_NAME, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    win.blit(text_surface, text_rect)

def draw_hangman(status):
    pygame.draw.line(win, BLACK, (100, 500), (300, 500), 5)
    pygame.draw.line(win, BLACK, (200, 500), (200, 100), 5)
    pygame.draw.line(win, BLACK, (200, 100), (350, 100), 5)
    pygame.draw.line(win, BLACK, (350, 100), (350, 150), 5)
    if status > 0: pygame.draw.circle(win, BLACK, (350, 180), 30, 3)
    if status > 1: pygame.draw.line(win, BLACK, (350, 210), (350, 320), 3)
    if status > 2: pygame.draw.line(win, BLACK, (350, 240), (300, 270), 3)
    if status > 3: pygame.draw.line(win, BLACK, (350, 240), (400, 270), 3)
    if status > 4: pygame.draw.line(win, BLACK, (350, 320), (300, 370), 3)
    if status > 5: pygame.draw.line(win, BLACK, (350, 320), (400, 370), 3)

def init_game():
    global word, guessed, hangman_status, letters, game_over, won
    word = random.choice(WORDS)
    guessed = []
    hangman_status = 0
    game_over = False
    won = False

    letters.clear()
    russian_alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    startx = round((WIDTH - (RADIUS * 2 + GAP) * 11) / 2)
    starty = 450
    for i in range(len(russian_alphabet)):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 11))
        y = starty + ((i // 11) * (GAP + RADIUS * 2))
        letters.append([x, y, russian_alphabet[i], True])

def draw(score, max_score):
    win.fill(WHITE)
    draw_text("Виселица", 48, BLACK, WIDTH // 2, 50)
    draw_text(f"Счёт: {score}", 28, BLACK, WIDTH - 150, 20)
    draw_text(f"Рекорд: {max_score}", 28, BLACK, WIDTH - 150, 60)

    # Слово
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    draw_text(display_word.strip(), 40, BLACK, WIDTH // 2, 200)

    # Кнопки
    for letter in letters:
        x, y, char, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            draw_text(char, 20, BLACK, x, y)

    draw_hangman(hangman_status)
    pygame.display.update()

def check_game_over():
    global game_over, won
    if hangman_status >= 6:
        game_over = True
    elif all(letter in guessed for letter in word):
        game_over = True
        won = True

# --- Игровой цикл ---
score = 0
max_score = 0
letters = []
init_game()
running = True

while running:
    clock.tick(FPS)
    draw(score, max_score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, char, visible = letter
                if visible:
                    dist = ((x - m_x) ** 2 + (y - m_y) ** 2) ** 0.5
                    if dist <= RADIUS:
                        letter[3] = False
                        guessed.append(char)
                        if char not in word:
                            hangman_status += 1
                        check_game_over()

    if game_over:
        pygame.time.delay(1000)
        if won:
            score += 1
            if score > max_score:
                max_score = score
        else:
            score = 0  # сброс счёта при проигрыше
        init_game()

pygame.quit()