import heapq  # Para usar la cola de prioridad (open list de A*)
import time   # Para medir el tiempo de ejecución
from modelo import reconstruct_path  # Para construir el camino desde la solución

# Heurística: Distancia Manhattan
def manhattan_distance(state, goal_state):
    distance = 0                                 # Inicializa la distancia total en 0
    for num in range(1, 9):                      # Recorre los números del 1 al 8 (el 0 es el espacio vacío)
        for i in range(3):                       # Recorre filas de la matriz
            for j in range(3):                   # Recorre columnas de la matriz
                if state[i][j] == num:           # Si encuentra el número en el estado actual
                    x1, y1 = i, j                # Guarda su posición actual
                if goal_state[i][j] == num:      # Si encuentra el número en el estado meta
                    x2, y2 = i, j                # Guarda su posición objetivo
        distance += abs(x1 - x2) + abs(y1 - y2)  # Suma la distancia Manhattan para ese número
    return distance                              # Devuelve la suma total

# Algoritmo A* (informado)
def astar(start, goal_state):
    start_time = time.time()                     # Guarda el tiempo de inicio
    open_set = []                               # Cola de prioridad para los nodos por expandir
    heapq.heappush(open_set, (0, start))        # Inserta el nodo inicial con prioridad 0
    visited = set()                             # Conjunto de estados ya visitados
    nodes_expanded = 0                          # Contador de nodos expandidos

    # Bucle principal de búsqueda
    while open_set:                             # Mientras haya nodos por expandir
        _, current = heapq.heappop(open_set)    # Extrae el nodo con menor f (prioridad)
        nodes_expanded += 1                     # Incrementa el contador de nodos expandidos

        if current.is_goal(goal_state):         # Si el nodo actual es el objetivo
            return reconstruct_path(current), nodes_expanded, time.time() - start_time  # Devuelve el camino, nodos expandidos y tiempo

        visited.add(current)                    # Marca el nodo actual como visitado

        # Genera hijos del nodo actual
        for child in current.generate_children():
            if child not in visited:            # Si el hijo no ha sido visitado
                g = child.depth                 # Costo desde el inicio hasta el hijo (profundidad)
                h = manhattan_distance(child.state, goal_state)  # Calcula la heurística
                f = g + h                       # Costo total estimado (f = g + h)
                heapq.heappush(open_set, (f, child))  # Añade el hijo a la cola de prioridad

    # Si no hay solución encontrada
    return None, nodes_expanded, time.time() - start_time  # Devuelve None y estadísticas