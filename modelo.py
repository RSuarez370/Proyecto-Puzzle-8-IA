import copy  # Importa el módulo copy para realizar copias profundas de listas (matrices)
import random  # Importa el módulo random para generar números aleatorios

# Estado meta del Puzzle 8 (el objetivo que el agente debe alcanzar)
GOAL_STATE = [
    [1, 2, 3],      # Primera fila del estado meta
    [8, 0, 4],      # Segunda fila (0 representa el espacio en blanco)
    [7, 6, 5]       # Tercera fila
]

# Clase que representa un estado del Puzzle 8
class Puzzle8:
    def __init__(self, state, parent=None, move="", depth=0):
        self.state = [row[:] for row in state]  # Copia profunda de la matriz de estado para evitar referencias compartidas
        self.parent = parent                # Nodo padre, usado para reconstruir el camino de solución
        self.move = move                    # Movimiento que llevó a este estado (por ejemplo: 'up', 'down', etc.)
        self.depth = depth                  # Profundidad del nodo en el árbol de búsqueda
        self.blank_pos = self.find_blank()  # Guarda la posición del "0" (espacio en blanco) en el tablero

    # Método para encontrar la posición del espacio en blanco (0)
    def find_blank(self):
        for i in range(3):              # Recorre las filas de la matriz (0 a 2)
            for j in range(3):          # Recorre las columnas de la matriz (0 a 2)
                if self.state[i][j] == 0:   # Si encuentra el 0 (espacio en blanco)
                    return i, j         # Retorna la posición como una tupla (fila, columna)

    # Genera los hijos del nodo actual con los movimientos posibles del espacio en blanco
    def generate_children(self):
        children = []                   # Lista para almacenar los hijos generados
        i, j = self.blank_pos           # Obtiene la posición actual del espacio en blanco

        # Define los movimientos posibles y sus nuevas posiciones
        moves = {
            'up': (i-1, j),             # Mover el espacio en blanco hacia arriba
            'down': (i+1, j),           # Mover hacia abajo
            'left': (i, j-1),           # Mover hacia la izquierda
            'right': (i, j+1)           # Mover hacia la derecha
        }

        # Intenta cada movimiento válido
        for move, (new_i, new_j) in moves.items():
            if 0 <= new_i < 3 and 0 <= new_j < 3:  # Solo si la nueva posición está dentro del tablero
                new_state = copy.deepcopy(self.state)  # Copia profunda del estado actual para modificarlo sin afectar el original
                # Intercambia el 0 con el número en la nueva posición
                new_state[i][j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[i][j]
                # Crea un nuevo objeto Puzzle8 como hijo, con el nuevo estado, el nodo actual como padre, el movimiento realizado y la nueva profundidad
                children.append(Puzzle8(new_state, self, move, self.depth + 1))
        return children                 # Devuelve la lista de hijos generados

    # Verifica si el estado actual es igual al estado meta
    def is_goal(self, goal_state):
        return self.state == goal_state # Retorna True si el estado actual es igual al estado meta

    def __eq__(self, other):
        if not isinstance(other, Puzzle8):   # Verifica si el otro objeto es una instancia de Puzzle8
            return False
        return self.state == other.state     # Compara los estados para igualdad

    # Permite que el objeto se pueda usar en estructuras como sets y diccionarios
    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.state))  # Convierte la matriz en tuplas para poder hashearla

    def __lt__(self, other):
        # Compara por profundidad solo para desempatar en estructuras como heapq
        return self.depth < other.depth

# Reconstruye el camino desde el nodo inicial hasta el nodo actual (solución)
def reconstruct_path(node):
    path = []                           # Lista para almacenar el camino de movimientos y estados
    while node.parent:                  # Mientras el nodo tenga un padre (no sea el inicial)
        path.append((node.move, node.state))  # Agrega el movimiento y el estado actual al camino
        node = node.parent              # Retrocede al nodo padre
    path.append(("start", node.state))  # Agrega el estado inicial con el movimiento "start"
    path.reverse()                      # Invierte la lista para que vaya del inicio al final
    return path                         # Devuelve el camino reconstruido

# Cuenta las inversiones en una lista plana del estado (para validar si es resoluble)
def count_inversions(flat_state):
    inv_count = 0                       # Inicializa el contador de inversiones
    nums = [n for n in flat_state if n != 0]  # Elimina el 0 de la lista (no se cuenta en las inversiones)
    for i in range(len(nums)):          # Recorre cada elemento
        for j in range(i + 1, len(nums)):   # Compara con los elementos siguientes
            if nums[i] > nums[j]:       # Si hay una inversión (un número mayor antes que uno menor)
                inv_count += 1          # Incrementa el contador
    return inv_count                    # Devuelve el número total de inversiones

# Determina si un estado es resoluble usando la cantidad de inversiones
def is_solvable(state):
    flat = sum(state, [])               # Convierte la matriz 3x3 en una lista plana
    return count_inversions(flat) % 2 == 0  # Si las inversiones son pares, el puzzle es resoluble

# Genera un estado aleatorio que sea resoluble y diferente al estado meta
def generate_solvable_puzzle(moves=30):
    import random
    while True:                         # Bucle hasta encontrar un estado válido
        state = [row[:] for row in GOAL_STATE]  # Copia profunda del estado meta
        puzzle = Puzzle8(state)         # Crea un objeto Puzzle8 con el estado actual
        last_move = None                # Inicializa el último movimiento realizado
        for _ in range(moves):          # Realiza una cantidad de movimientos aleatorios
            children = puzzle.generate_children()  # Genera los hijos posibles
            # Evita deshacer el último movimiento (no volver atrás)
            if last_move:
                children = [child for child in children if child.move != last_move]
            if not children:            # Si no hay hijos válidos, genera de nuevo
                children = puzzle.generate_children()
            next_puzzle = random.choice(children)  # Elige un hijo aleatorio
            last_move = next_puzzle.move           # Actualiza el último movimiento
            puzzle = next_puzzle                   # Avanza al siguiente estado
        # Devuelve solo la matriz de estado generada
        generated_state = [row[:] for row in puzzle.state]
        # Si el estado generado es igual al meta, repite el proceso
        if generated_state != GOAL_STATE:
            return generated_state         # Devuelve el estado generado si es diferente al meta