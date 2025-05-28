import pygame                # Importa la librería gráfica pygame
import sys                   # Importa sys para salir del programa
import threading             # Importa threading para ejecutar la resolución en un hilo aparte
from interfaz import draw_puzzle, PUZZLE_START_X, PUZZLE_SIZE  # Asegúrate de importar PUZZLE_START_X y PUZZLE_SIZE
from modelo import Puzzle8, GOAL_STATE, generate_solvable_puzzle  # Importa la clase del puzzle, el estado meta y el generador de puzzles resolubles
from agente_no_informado import bfs   # Importa el agente BFS
from agente_informado import astar    # Importa el agente A*

SCREEN_SIZE = 700            # Define el tamaño de la ventana (cuadrada)
FONDO = (30, 30, 30)         # Color de fondo oscuro
BARRA_Y = 40  # Distancia desde el borde superior
BARRA_ALTURA = 38  # Altura de la barra
BARRA_EXTRA = 100  # Puedes ajustar este valor

barra_x = PUZZLE_START_X - BARRA_EXTRA // 2
barra_w = PUZZLE_SIZE + BARRA_EXTRA

def main():
    pygame.init()            # Inicializa pygame
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))  # Crea la ventana principal
    pygame.display.set_caption("Puzzle 8 - Agente Inteligente")   # Título de la ventana

    # Estado inicial aleatorio y resoluble
    puzzle_state = generate_solvable_puzzle()    # Genera un tablero inicial resoluble aleatorio
    print("Estado inicial:")                     # Imprime el estado inicial en consola
    for fila in puzzle_state:
        print(fila)
    print("Estado meta:")                        # Imprime el estado meta en consola
    for fila in GOAL_STATE:
        print(fila)
    agent_selected = False       # Indica si ya se seleccionó un agente
    agent_type = None            # Tipo de agente seleccionado ("BFS" o "A*")
    solved = False               # Indica si el puzzle ya fue resuelto
    path = []                    # Lista de pasos de la solución
    animating = False            # Indica si se está animando la solución
    animation_index = 0          # Índice del paso actual en la animación
    solving = False              # Indica si el agente está resolviendo el puzzle

    movimientos = 0              # Número de movimientos de la solución
    tiempo = 0                   # Tiempo que tardó en resolver
    nodos_expandidos = 0         # Nodos expandidos por el agente

    # Función que ejecuta la resolución del puzzle en un hilo aparte
    def resolver_puzzle():
        nonlocal path, animating, animation_index, solving, movimientos, tiempo, solved, nodos_expandidos
        solving = True
        start_node = Puzzle8(puzzle_state)       # Crea el nodo inicial
        if agent_type == "BFS":                  # Si el agente es BFS
            resultado = bfs(start_node, GOAL_STATE)
        else:                                   # Si el agente es A*
            resultado = astar(start_node, GOAL_STATE)
        if resultado and resultado[0]:           # Si se encontró solución
            path, nodos_expandidos, tiempo = resultado
            movimientos = max(0, len(path) - 1)  # Calcula el número de movimientos
            animating = True                     # Activa la animación
            animation_index = 0                  # Reinicia el índice de animación
            solved = False                       # Marca como no resuelto (hasta terminar la animación)
        else:
            print("No se encontró solución.")    # Si no hay solución, lo indica
            path = []
            movimientos = 0
            tiempo = 0
            solved = True
        solving = False                          # Marca que terminó la resolución

    # Función para reiniciar todas las variables y generar un nuevo puzzle
    def reiniciar_estado():
        nonlocal agent_selected, agent_type, solved, path, animating, animation_index, solving
        nonlocal movimientos, tiempo, nodos_expandidos, puzzle_state
        agent_selected = False
        agent_type = None
        solved = False
        path = []
        animating = False
        animation_index = 0
        solving = False
        movimientos = 0
        tiempo = 0
        nodos_expandidos = 0
        # Tablero aleatorio resoluble
        puzzle_state = generate_solvable_puzzle()

    running = True                               # Controla el bucle principal
    font_bar = pygame.font.SysFont(None, 36)     # Fuente para la barra superior

    while running:
        screen.fill(FONDO)  # Fondo oscuro, solo una vez

        if not agent_selected:
            # Dibuja botones de selección de agente
            from interfaz import draw_menu
            bfs_button, astar_button = draw_menu(screen)
            boton_volver = None  # No hay botón volver en el menú principal
        else:
            # Dibuja el tablero según el estado de la animación
            if animating and path:
                draw_puzzle(screen, path[animation_index][1])    # Dibuja el paso actual de la animación
            elif path and solved:
                draw_puzzle(screen, path[-1][1])                 # Dibuja el estado final
            else:
                draw_puzzle(screen, puzzle_state)                # Dibuja el estado actual

            # Dibuja el botón "Volver al menú"
            boton_volver = pygame.Rect(SCREEN_SIZE - 210, SCREEN_SIZE - 70, 190, 50)
            pygame.draw.rect(screen, (200, 60, 60), boton_volver, border_radius=15)
            font_btn = pygame.font.SysFont(None, 32)
            texto_volver = font_btn.render("Volver al menú", True, (255, 255, 255))
            texto_rect = texto_volver.get_rect(center=boton_volver.center)
            screen.blit(texto_volver, texto_rect)

            # Barra superior SOLO después de elegir agente
            pygame.draw.rect(
    screen,
    (12, 126, 126),  # Color de la barra superior
    (barra_x, BARRA_Y, barra_w, BARRA_ALTURA),
    border_radius=16
)
            font_bar = pygame.font.SysFont(None, 22)
            texto_barra = font_bar.render(
    f"Tiempo: {tiempo:.4f}s   Movimientos: {movimientos}   Nodos expandidos: {nodos_expandidos}",
    True,
    (255, 255, 255)
)
            texto_rect = texto_barra.get_rect(center=(barra_x + barra_w // 2, BARRA_Y + BARRA_ALTURA // 2))
            screen.blit(texto_barra, texto_rect)

            # Botón "Volver al menú"
            boton_volver = pygame.Rect(SCREEN_SIZE - 210, SCREEN_SIZE - 70, 190, 50)
            pygame.draw.rect(screen, (0, 51, 153), boton_volver, border_radius=15)  # Color solicitado
            font_btn = pygame.font.SysFont(None, 32)
            texto_volver = font_btn.render("Volver al menú", True, (255, 255, 255))
            texto_rect = texto_volver.get_rect(center=boton_volver.center)
            screen.blit(texto_volver, texto_rect)

        pygame.display.flip()                    # Actualiza la pantalla

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False                  # Sale del bucle si se cierra la ventana

            if not agent_selected and event.type == pygame.MOUSEBUTTONDOWN:
                if bfs_button and bfs_button.collidepoint(event.pos):
                    reiniciar_estado()           # Reinicia todo antes de lanzar el agente
                    agent_type = "BFS"
                    agent_selected = True
                    if not solving:
                        threading.Thread(target=resolver_puzzle, daemon=True).start()
                elif astar_button and astar_button.collidepoint(event.pos):
                    reiniciar_estado()
                    agent_type = "A*"
                    agent_selected = True
                    if not solving:
                        threading.Thread(target=resolver_puzzle, daemon=True).start()
            elif agent_selected and event.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver and boton_volver.collidepoint(event.pos):
                    reiniciar_estado()           # Reinicia todo y genera nuevo puzzle

        # Animación paso a paso
        if animating and path:
            pygame.time.wait(450)               # Espera 410 ms entre cada paso de la animación
            animation_index += 1
            if animation_index >= len(path):     # Si termina la animación
                animating = False
                solved = True
                animation_index = len(path) - 1  # Deja el índice en el último paso

    pygame.quit()                               # Cierra pygame
    sys.exit()                                  # Sale del programa

if __name__ == "__main__":
    main()                                      # Llama a la función principal