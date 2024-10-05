import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 400, 650  # Incrementar altura para botón "Resolver"
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Mastermind')

# Definir colores
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

# Colores disponibles para los pines
COLORS = [RED, BLUE, GREEN, YELLOW]

# Parámetros del juego
ROWS = 10  # Número de intentos
COLUMNS = 4  # Número de colores por intento
PEG_RADIUS = 20
GAP = 10
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40

# Generar código secreto aleatorio
def generate_code():
    return [random.choice(COLORS) for _ in range(COLUMNS)]

# Dibujar tablero del juego
def draw_board(guesses, feedback, current_guess):
    screen.fill(WHITE)

    # Dibujar intentos anteriores
    for row in range(ROWS):
        y = HEIGHT - 100 - (row + 1) * (PEG_RADIUS * 2 + GAP)  # Ajustar para el botón
        for col in range(COLUMNS):
            x = col * (PEG_RADIUS * 2 + GAP) + 50
            if row < len(guesses):
                color = guesses[row][col]
            else:
                color = GRAY if row == len(guesses) else BLACK
            pygame.draw.circle(screen, color, (x, y), PEG_RADIUS)

        # Dibujar retroalimentación
        if row < len(feedback):
            correct_pos, correct_color = feedback[row]
            for i in range(correct_pos):
                pygame.draw.circle(screen, BLACK, (COLUMNS * 70 + i * 20, y), PEG_RADIUS // 2)
            for i in range(correct_color):
                pygame.draw.circle(screen, WHITE, (COLUMNS * 70 + (correct_pos + i) * 20, y), PEG_RADIUS // 2)

    # Dibujar intento actual
    y = HEIGHT - 100 - (len(guesses) + 1) * (PEG_RADIUS * 2 + GAP)
    for col in range(COLUMNS):
        x = col * (PEG_RADIUS * 2 + GAP) + 50
        pygame.draw.circle(screen, current_guess[col], (x, y), PEG_RADIUS)

    # Dibujar la barra de selección de colores
    for i, color in enumerate(COLORS):
        pygame.draw.circle(screen, color, (i * 100 + 50, HEIGHT - 80), PEG_RADIUS)

    # Dibujar botón "Resolver"
    pygame.draw.rect(screen, GRAY, (WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - 50, BUTTON_WIDTH, BUTTON_HEIGHT))
    font = pygame.font.SysFont(None, 30)
    text = font.render("Resolver", True, BLACK)
    screen.blit(text, (WIDTH // 2 - BUTTON_WIDTH // 2 + 10, HEIGHT - 45))

# Evaluar intento con el código
def evaluate_guess(guess, code):
    correct_pos = sum([1 for i in range(COLUMNS) if guess[i] == code[i]])
    correct_color = sum([min(guess.count(c), code.count(c)) for c in COLORS]) - correct_pos
    return correct_pos, correct_color

# Resolver el código automáticamente, paso a paso
def auto_solve(code):
    guesses = []
    feedback = []
    possible_guesses = [[r, g, b, y] for r in COLORS for g in COLORS for b in COLORS for y in COLORS]

    for guess in possible_guesses:
        correct_pos, correct_color = evaluate_guess(guess, code)
        guesses.append(guess.copy())
        feedback.append((correct_pos, correct_color))
        
        # Dibujar el estado actual paso a paso
        draw_board(guesses, feedback, guess)
        pygame.display.update()
        
        # Pausar para mostrar el proceso
        pygame.time.delay(500)
        
        if correct_pos == COLUMNS:
            return guesses, feedback

# Lógica principal del juego
def main():
    running = True
    guesses = []
    feedback = []
    secret_code = generate_code()
    current_guess = [BLACK] * COLUMNS
    current_pos = 0
    current_row = 0
    solved = False

    while running:
        draw_board(guesses, feedback, current_guess)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Selección de colores con el ratón
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Seleccionar posición en el intento actual
                y = HEIGHT - 100 - (current_row + 1) * (PEG_RADIUS * 2 + GAP)
                for col in range(COLUMNS):
                    x = col * (PEG_RADIUS * 2 + GAP) + 50
                    if x - PEG_RADIUS < mouse_x < x + PEG_RADIUS and y - PEG_RADIUS < mouse_y < y + PEG_RADIUS:
                        current_pos = col

                # Seleccionar un color desde la barra de selección
                if HEIGHT - 80 - PEG_RADIUS < mouse_y < HEIGHT - 80 + PEG_RADIUS:
                    if 50 - PEG_RADIUS < mouse_x < 50 + PEG_RADIUS:
                        current_guess[current_pos] = RED
                    elif 150 - PEG_RADIUS < mouse_x < 150 + PEG_RADIUS:
                        current_guess[current_pos] = BLUE
                    elif 250 - PEG_RADIUS < mouse_x < 250 + PEG_RADIUS:
                        current_guess[current_pos] = GREEN
                    elif 350 - PEG_RADIUS < mouse_x < 350 + PEG_RADIUS:
                        current_guess[current_pos] = YELLOW

                # Detectar clic en el botón "Resolver"
                if WIDTH // 2 - BUTTON_WIDTH // 2 < mouse_x < WIDTH // 2 + BUTTON_WIDTH // 2 and HEIGHT - 50 < mouse_y < HEIGHT - 10:
                    guesses, feedback = auto_solve(secret_code)
                    solved = True

            # Confirmar intento con ENTER
            if event.type == pygame.KEYDOWN and not solved:
                if event.key == pygame.K_RETURN and current_row < ROWS:
                    if BLACK not in current_guess:
                        guesses.append(current_guess.copy())
                        feedback.append(evaluate_guess(current_guess, secret_code))
                        current_row += 1
                        current_guess = [BLACK] * COLUMNS

        # Condición de victoria o derrota
        if len(feedback) > 0 and feedback[-1][0] == COLUMNS:
            print("¡Ganaste!")
            pygame.time.delay(1000)
            running = False
        elif current_row >= ROWS:
            print(f"Perdiste. El código era: {secret_code}")
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
