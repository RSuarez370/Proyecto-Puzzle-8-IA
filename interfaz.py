import pygame  # Importa la librería gráfica pygame para crear la interfaz
import time    # Importa time para manejar pausas en la animación

# Tamaño de la pantalla (cuadrado) y la cuadrícula
SCREEN_SIZE = 700  # Define el tamaño de la ventana principal (700x700 píxeles)
CELL_SIZE = 140    # Tamaño de cada celda del puzzle (140x140 píxeles)
PUZZLE_SIZE = 3 * CELL_SIZE  # Tamaño total del puzzle (3x3 celdas)

# Posición de inicio del puzzle dentro de la cuadrícula (centrado)
PUZZLE_START_X = (SCREEN_SIZE - PUZZLE_SIZE) // 2  # Coordenada X inicial del puzzle
PUZZLE_START_Y = (SCREEN_SIZE - PUZZLE_SIZE) // 2  # Coordenada Y inicial del puzzle

# Colores usados en la interfaz (en formato RGB)
FONDO = (26,26,26)         # Color de fondo de la ventana
WHITE = (255, 255, 255)    # Blanco
BLACK = (0, 0, 0)          # Negro
GRAY = (180, 180, 180)     # Gris
BLUE = (0, 120, 215)       # Azul
GREEN = (34, 139, 34)      # Verde
RED = (200, 0, 0)          # Rojo

# Inicializa pygame y la fuente por defecto
pygame.init()  # Inicializa todos los módulos de pygame
FONT = pygame.font.SysFont(None, 40)  # Fuente predeterminada de tamaño 40

# Dibuja el estado actual del puzzle (solo en una sección 3x3 del grid)
def draw_puzzle(screen, puzzle_state):
    marco_color = (19, 70, 71)         # Color del marco exterior del puzzle
    pieza_color = (12, 126, 126)       # Color de las piezas del puzzle
    marco_grosor = 18                  # Grosor del marco exterior
    PADDING = 8                        # Espacio entre celdas

    screen.fill(FONDO)                 # Rellena la pantalla con el color de fondo

    # Dibuja el marco centrado alrededor del puzzle
    marco_rect = pygame.Rect(
        PUZZLE_START_X - marco_grosor,                 # X inicial del marco
        PUZZLE_START_Y - marco_grosor,                 # Y inicial del marco
        PUZZLE_SIZE + 2 * marco_grosor,                # Ancho del marco
        PUZZLE_SIZE + 2 * marco_grosor                 # Alto del marco
    )
    pygame.draw.rect(screen, marco_color, marco_rect, border_radius=28)  # Dibuja el fondo del marco
    pygame.draw.rect(screen, marco_color, marco_rect, width=marco_grosor, border_radius=28)  # Dibuja el borde

    # Dibuja las celdas separadas por PADDING
    for i in range(3):                        # Recorre las filas
        for j in range(3):                    # Recorre las columnas
            value = puzzle_state[i][j]        # Obtiene el valor de la celda (0 es vacío)
            x = PUZZLE_START_X + j * CELL_SIZE + PADDING // 2  # Calcula la posición X de la celda
            y = PUZZLE_START_Y + i * CELL_SIZE + PADDING // 2  # Calcula la posición Y de la celda
            rect = pygame.Rect(
                x,
                y,
                CELL_SIZE - PADDING,          # Ancho de la celda
                CELL_SIZE - PADDING           # Alto de la celda
            )

            if value != 0:                    # Si la celda no es el espacio vacío
                pygame.draw.rect(screen, pieza_color, rect, border_radius=24)  # Dibuja la pieza
                text = FONT.render(str(value), True, WHITE)                    # Renderiza el número
                screen.blit(text, text.get_rect(center=rect.center))           # Dibuja el número centrado
            else:
                pygame.draw.rect(screen, marco_color, rect, border_radius=24)  # Celda vacía igual al marco

# Dibuja el menú de selección de agente (BFS o A*)
def draw_menu(screen):
    screen.fill(FONDO)  # Rellena la pantalla con el color de fondo

    # --- Título grande y blanco ---
    titulo_font = pygame.font.SysFont("champion HTF heavyweight", 80, bold=False)  # Fuente para el título
    title = titulo_font.render("Puzzle 8", True, WHITE)                           # Renderiza el texto del título
    screen.blit(title, (SCREEN_SIZE // 2 - title.get_width() // 2, 60))           # Dibuja el título centrado arriba

    # --- Texto "Seleccione un Agente" centrado ---
    subtitulo_font = pygame.font.SysFont(None, 32)                                # Fuente para el subtítulo
    subtitulo = subtitulo_font.render("Seleccione un Agente", True, WHITE)        # Renderiza el subtítulo
    y_subtitulo = 210                                                             # Posición Y del subtítulo
    screen.blit(subtitulo, (SCREEN_SIZE // 2 - subtitulo.get_width() // 2, y_subtitulo))  # Centra el subtítulo

    # --- Botones centrados horizontalmente ---
    boton_color = (12, 126, 126)      # Color de los botones
    boton_ancho = 340                 # Ancho de los botones
    boton_alto = 60                   # Alto de los botones
    espacio_entre = 30                # Espacio vertical entre botones

    x_boton = (SCREEN_SIZE - boton_ancho) // 2           # Centra los botones horizontalmente
    y_boton1 = y_subtitulo + 40                          # Posición Y del primer botón
    y_boton2 = y_boton1 + boton_alto + espacio_entre     # Posición Y del segundo botón

    bfs_button = pygame.Rect(x_boton, y_boton1, boton_ancho, boton_alto)      # Rectángulo del botón BFS
    astar_button = pygame.Rect(x_boton, y_boton2, boton_ancho, boton_alto)    # Rectángulo del botón A*

    pygame.draw.rect(screen, boton_color, bfs_button, border_radius=20)       # Dibuja el botón BFS
    pygame.draw.rect(screen, boton_color, astar_button, border_radius=20)     # Dibuja el botón A*

    btn_font = pygame.font.SysFont(None, 30)                                  # Fuente para el texto de los botones
    bfs_text = btn_font.render("Agente No Informado (BFS)", True, WHITE)      # Texto del botón BFS
    bfs_text_rect = bfs_text.get_rect(center=bfs_button.center)               # Centra el texto en el botón
    screen.blit(bfs_text, bfs_text_rect)                                      # Dibuja el texto del botón BFS

    astar_text = btn_font.render("Agente Informado (A*)", True, WHITE)        # Texto del botón A*
    astar_text_rect = astar_text.get_rect(center=astar_button.center)          # Centra el texto en el botón
    screen.blit(astar_text, astar_text_rect)                                  # Dibuja el texto del botón A*

    # --- Pie de página alineado a la derecha ---
    pie_color = (19, 70, 71)                                                  # Color del pie de página
    pie_alto = 36                                                             # Alto del pie de página
    pygame.draw.rect(screen, pie_color, (0, SCREEN_SIZE - pie_alto, SCREEN_SIZE, pie_alto))  # Dibuja el fondo del pie
    pie_font = pygame.font.SysFont(None, 22)                                  # Fuente para el pie de página
    pie_text = pie_font.render("Desarrollado por: Richard Suárez, C.I:30.331.087", True, WHITE)  # Texto del pie
    pie_text_rect = pie_text.get_rect()                                       # Rectángulo del texto
    pie_text_rect.bottomright = (SCREEN_SIZE - 12, SCREEN_SIZE - 8)           # Posición del texto en la esquina inferior derecha
    screen.blit(pie_text, pie_text_rect)                                      # Dibuja el texto del pie de página

    return bfs_button, astar_button                                           # Devuelve los rectángulos de los botones para detectar clics

# Dibuja el botón de "Iniciar"
def draw_start_button(screen):
    screen.fill(FONDO)                                   # Rellena la pantalla con el color de fondo
    start_button = pygame.Rect(450, 30, 120, 40)         # Define el rectángulo del botón de iniciar
    pygame.draw.rect(screen, RED, start_button)          # Dibuja el botón en rojo
    screen.blit(FONT.render("Iniciar", True, WHITE), (start_button.x + 15, start_button.y + 5))  # Dibuja el texto "Iniciar"
    return start_button                                  # Devuelve el rectángulo del botón para detectar clics

# Anima la solución paso a paso en pantalla
def animate_solution(screen, path, delay=0.5):
    for move, state in path:                 # Recorre cada paso de la solución (movimiento y estado)
        screen.fill(FONDO)                   # Rellena la pantalla con el color de fondo
        draw_puzzle(screen, state)           # Dibuja el estado actual del puzzle
        pygame.display.flip()                # Actualiza la pantalla para mostrar los cambios
        time.sleep(delay)                    # Espera un tiempo antes de mostrar el siguiente paso