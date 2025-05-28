from collections import deque           # Importa deque para usar una cola eficiente (FIFO)
import time                             # Importa time para medir el tiempo de ejecución
from modelo import reconstruct_path     # Importa la función para reconstruir el camino de solución

# Implementa la búsqueda en anchura (BFS) para el Puzzle 8
def bfs(start, goal):
    start_time = time.time()            # Guarda el tiempo de inicio de la búsqueda
    visited = set()                     # Conjunto para registrar los nodos ya visitados
    queue = deque([start])              # Cola de nodos por expandir, inicia con el nodo inicial
    nodes_expanded = 0                  # Contador de nodos expandidos

    visited.add(start)                  # Marca el nodo inicial como visitado

    while queue:                        # Mientras haya nodos por expandir en la cola
        node = queue.popleft()          # Extrae el primer nodo de la cola (FIFO)
        nodes_expanded += 1             # Incrementa el contador de nodos expandidos

        if node.is_goal(goal):          # Si el nodo actual es el objetivo
            end_time = time.time()      # Guarda el tiempo de finalización
            path = reconstruct_path(node)   # Reconstruye el camino desde el inicio hasta el objetivo
            return path, nodes_expanded, end_time - start_time  # Devuelve el camino, nodos expandidos y tiempo

        for child in node.generate_children():   # Genera todos los hijos posibles del nodo actual
            if child not in visited:             # Si el hijo no ha sido visitado aún
                queue.append(child)              # Lo agrega a la cola para expandirlo después
                visited.add(child)               # Lo marca como visitado

        if nodes_expanded % 1000 == 0:           # Cada 1000 nodos expandidos
            print(f"Nodos expandidos: {nodes_expanded}")  # Imprime el progreso

    return None, nodes_expanded, time.time() - start_time # Si no se encuentra solución, devuelve None y estadísticas