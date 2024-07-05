"""Busqueda de Ruta"""
class Nodo:
    def __init__(self, x, y, g_cost=0, h_cost=0): #Inicializa un nodo con sus coordenadas (x, y) y los costos g_cost y h_cost
        self.x = x # Coordenada x del nodo
        self.y = y # Coordenada y del nodo
        self.g_cost = g_cost # Costo desde el nodo inicial hasta este nodo
        self.h_cost = h_cost # Costo estimado desde este nodo hasta el nodo final
        self.padre = None # Nodo padre (para reconstruir el camino)

    @property
    def f_cost(self): # Calcula el costo total f_cost, la suma de g_cost y h_cost.
        return self.g_cost + self.h_cost

def calcular_h_cost(nodo_actual, nodo_final): 
     # Calcula la heurística usando la distancia de Manhattan
    return abs(nodo_actual.x - nodo_final.x) + abs(nodo_final.y - nodo_actual.y)

def obtener_vecinos(nodo, mapa): # Encuentra los vecinos transitables de un nodo dado 
    # y verifica que estén dentro de los límites del mapa y que no sean obstáculos (valor 0 en el mapa).
    vecinos = [] # Lista para almacenar los vecinos transitables
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, Abajo, Izquierda, Derecha
    for dx, dy in direcciones:
        nuevo_x, nuevo_y = nodo.x + dx, nodo.y + dy # Coordenadas del vecino potencial
        # Verifica si el vecino está dentro de los límites del mapa y es transitable
        if 0 <= nuevo_x < len(mapa) and 0 <= nuevo_y < len(mapa[0]) and mapa[nuevo_x][nuevo_y] == 0:
            vecinos.append(Nodo(nuevo_x, nuevo_y)) # Añade el vecino a la lista
    return vecinos # Retorna la lista de vecinos transitables

def a_estrella(mapa, inicio, fin):
    nodo_inicio = Nodo(inicio[0], inicio[1]) # Nodo inicial
    nodo_final = Nodo(fin[0], fin[1]) # Nodo final
    nodo_inicio.h_cost = calcular_h_cost(nodo_inicio, nodo_final) # Calcula la heurística para el nodo inicial
    
    abierta = [nodo_inicio] # Lista de nodos por explorar (inicialmente contiene solo el nodo inicial)
    cerrada = []  # Lista de nodos ya explorados

    while abierta: # Mientras haya nodos por explorar
        # Selecciona el nodo con el menor f_cost
        nodo_actual = min(abierta, key=lambda nodo: nodo.f_cost)
        abierta.remove(nodo_actual) # Mueve el nodo actual de la lista abierta a la cerrada
        cerrada.append(nodo_actual)
        
        # Si el nodo actual es el nodo final, reconstruye el camino y termina
        if nodo_actual.x == nodo_final.x and nodo_actual.y == nodo_final.y:
            camino = []
            while nodo_actual:
                camino.append((nodo_actual.x, nodo_actual.y)) # Añade las coordenadas del nodo al camino
                nodo_actual = nodo_actual.padre # Retrocede al nodo padre
            return camino[::-1]  # Invierte el camino para obtener el orden correcto
        
         # Obtiene los vecinos transitables del nodo actual
        vecinos = obtener_vecinos(nodo_actual, mapa) 
        for vecino in vecinos:
            if vecino in cerrada: # Si el vecino ya fue explorado, lo ignora
                continue

            # Calcula los costos g y h para el vecino
            vecino.g_cost = nodo_actual.g_cost + 1
            vecino.h_cost = calcular_h_cost(vecino, nodo_final)
            vecino.padre = nodo_actual # Establece el nodo actual como el padre del vecino

            if vecino not in abierta: # Si el vecino no está en la lista abierta, lo agrega
                abierta.append(vecino)
            else:
                # Si el vecino ya está en la lista abierta con un mayor g_cost, actualiza su g_cost y su nodo padre
                abierto_vecino = next(n for n in abierta if n.x == vecino.x and n.y == vecino.y)
                if vecino.g_cost < abierto_vecino.g_cost:
                    abierto_vecino.g_cost = vecino.g_cost
                    abierto_vecino.padre = nodo_actual
    return None  # Si no se encontró un camino, retorna None

def imprimir_mapa_con_ruta(mapa, ruta):
    mapa_con_ruta = [fila[:] for fila in mapa]  # Crear una copia del mapa
    for x, y in ruta:
        mapa_con_ruta[x][y] = '*'
    simbolos = {0: '.', 1: 'X', 2: 'X', 3: 'X', '*': '*'}
    for fila in mapa_con_ruta:
        linea = ' '.join([simbolos[celda] for celda in fila])
        print(linea)

def mostrar_mapa(mapa):
    simbolos = {0: '.', 1: 'X', 2: 'X', 3: 'X'}
    for fila in mapa:
        linea = ' '.join([simbolos[celda] for celda in fila])
        print(linea)

def agregar_obstaculo(mapa, x, y, tipo_obstaculo=1):
    if 0 <= x < len(mapa) and 0 <= y < len(mapa[0]):
        mapa[x][y] = tipo_obstaculo
    else:
        print("Coordenadas fuera del rango del mapa.")

def ingresar_punto_inicio(mapa):
    while True:
        x = int(input("Ingrese la coordenada x del punto de inicio: "))
        y = int(input("Ingrese la coordenada y del punto de inicio: "))
        if 0 <= x < len(mapa) and 0 <= y < len(mapa[0]) and mapa[x][y] == 0:
            return (x, y)
        else:
            print("Coordenadas inválidas o punto de inicio en un obstáculo. Inténtelo de nuevo.")

def ingresar_punto_fin(mapa):
    while True:
        x = int(input("Ingrese la coordenada x del punto de fin: "))
        y = int(input("Ingrese la coordenada y del punto de fin: "))
        if 0 <= x < len(mapa) and 0 <= y < len(mapa[0]) and mapa[x][y] == 0:
            return (x, y)
        else:
            print("Coordenadas inválidas o punto de fin en un obstáculo. Inténtelo de nuevo.")

# Mapa inicial
mapa = [
    [0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

print("Mapa inicial:")
mostrar_mapa(mapa)

# Permitir al usuario agregar obstáculos
while True:
    agregar = input("¿Desea agregar un obstáculo? (s/n): ").lower()
    if agregar == 's':
        x = int(input("Ingrese la coordenada x del obstáculo: "))
        y = int(input("Ingrese la coordenada y del obstáculo: "))
        tipo_obstaculo = int(input("Ingrese el tipo de obstáculo (1, 2, o 3): "))
        agregar_obstaculo(mapa, x, y, tipo_obstaculo)
        print("\nMapa después de agregar un obstáculo en ({}, {}):".format(x, y))
        mostrar_mapa(mapa)
    else:
        break

# Ingresar puntos de inicio y fin
punto_inicio = ingresar_punto_inicio(mapa)
print("\nPunto de inicio:", punto_inicio)

punto_fin = ingresar_punto_fin(mapa)
print("Punto de fin:", punto_fin)

# Encontrar la ruta
ruta = a_estrella(mapa, punto_inicio, punto_fin)

# Imprimir el mapa con la ruta
if ruta:
    print("\nRuta encontrada:")
    imprimir_mapa_con_ruta(mapa, ruta)
else:
    print("No se encontró una ruta.")
