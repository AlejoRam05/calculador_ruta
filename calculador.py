"""ENCONTRAR UNA RUTA, las manera que usa un ser humano es 
haciendo una suposicion de donde se encuntra el objetivo desde el punto A y el punto B, luego recorre
una maquina debe saber la distancia de A a B, pero el mismo no puede saltarse ciertos procesos
eso provoca visitar lugares previos al objetivo"""

def obtener_entrada(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            if valor <= 10:
                raise ValueError("El valor debe ser superior a 10.")
            return valor
        except ValueError as e:
            print(e)

FILAS = obtener_entrada("Ingrese un número de filas (superior a 10): ")
COLUMNAS = obtener_entrada("Ingrese un número de columnas (superior a 10): ")

EDIFICIO = 1

def obtener_posicion(mensaje, FILAS, COLUMNAS, exclusion=None):
    while True:
        try:
            fila = int(input(f"Ingrese la fila para {mensaje} (0 a {FILAS-1}): "))
            columna = int(input(f"Ingrese la columna para {mensaje} (0 a {COLUMNAS-1}): "))
            if 0 <= fila < FILAS and 0 <= columna < COLUMNAS:
                if exclusion and (fila, columna) == exclusion:
                    raise ValueError("La posición no puede coincidir con la de exclusión.")
                return (fila, columna)
            else:
                raise ValueError("La posición debe estar dentro de los límites de la matriz.")
        except ValueError as e:
            print(e)

STAR = obtener_posicion("el inicio (STAR)", FILAS, COLUMNAS)
OBJETIVO = obtener_posicion("el objetivo", FILAS, COLUMNAS, exclusion=STAR)

def obtener_obstaculos(FILAS, COLUMNAS, matriz, STAR, OBJETIVO):
    obstaculos = []
    while True:
        try:
            num_obstaculos = int(input("Ingrese el número de obstáculos: "))
            for _ in range(num_obstaculos):
                while True:
                    obstaculo = obtener_posicion("el obstáculo", FILAS, COLUMNAS)
                    if obstaculo != STAR and obstaculo != OBJETIVO and matriz[obstaculo[0]][obstaculo[1]] == 0:
                        obstaculos.append(obstaculo)
                        break
                    else:
                        print("El obstáculo no puede estar en la posición de inicio, en el objetivo o en un edificio.")
            return obstaculos
        except ValueError as e:
            print(e)

class Nodo:
    def __init__(self, posicion, parent=None):
        self.posicion = posicion
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.posicion == other.posicion

def heuristica(nodo_actual, nodo_objetivo):
    return abs(nodo_actual.posicion[0] - nodo_objetivo.posicion[0]) + abs(nodo_actual.posicion[1] - nodo_objetivo.posicion[1])

movimientos = [(0, -1), (0, 1), (-1, 0), (1, 0)]

def generar_matriz(FILAS, COLUMNAS, EDIFICIO):
    matriz = []
    for i in range(FILAS):
        fila = []
        for j in range(COLUMNAS):
            if j % 2 == 1 and i % 2 == 1:
                fila.append(EDIFICIO)  # Representa un edificio
            else:
                fila.append(0)  # Representa un camino libre
        matriz.append(fila)
    return matriz

def a_estrella(inicio, fin, FILAS, COLUMNAS, matriz):
    nodo_inicio = Nodo(inicio)
    nodo_fin = Nodo(fin)

    lista_abierta = []
    lista_cerrada = []

    lista_abierta.append(nodo_inicio)

    while lista_abierta:
        nodo_actual = min(lista_abierta, key=lambda nodo: nodo.f)
        lista_abierta.remove(nodo_actual)
        lista_cerrada.append(nodo_actual)

        if nodo_actual == nodo_fin:
            camino = []
            actual = nodo_actual
            while actual:
                camino.append(actual.posicion)
                actual = actual.parent
            return camino[::-1]

        hijos = []
        for movimiento in movimientos:
            posicion_nueva = (nodo_actual.posicion[0] + movimiento[0], nodo_actual.posicion[1] + movimiento[1])
            if 0 <= posicion_nueva[0] < FILAS and 0 <= posicion_nueva[1] < COLUMNAS:
                if matriz[posicion_nueva[0]][posicion_nueva[1]] == 0:  # Verificar que no hay un obstáculo o edificio
                    nodo_nuevo = Nodo(posicion_nueva, nodo_actual)
                    hijos.append(nodo_nuevo)

        for hijo in hijos:
            if hijo in lista_cerrada:
                continue

            hijo.g = nodo_actual.g + 1
            hijo.h = heuristica(hijo, nodo_fin)
            hijo.f = hijo.g + hijo.h

            if hijo in lista_abierta:
                index = lista_abierta.index(hijo)
                if hijo.g < lista_abierta[index].g:
                    lista_abierta[index].g = hijo.g
                    lista_abierta[index].f = hijo.f
                    lista_abierta[index].parent = nodo_actual
            else:
                lista_abierta.append(hijo)

    return None

def visualizar(FILAS, COLUMNAS, OBJETIVO, STAR, matriz, camino):
    for i in range(FILAS):
        for j in range(COLUMNAS):
            print(i,j, end=" ")

            if matriz[i][j] == 1:
                print("⏹", end=" ")
            elif (i, j) == STAR:
                print("🚗", end=" ")
            elif (i, j) == OBJETIVO:
                print("❗", end=" ")
            elif camino and (i, j) in camino:
                print("🚩", end=" ")
            else:
                print(".", end=" ")
        print()
    print()

matriz = generar_matriz(FILAS, COLUMNAS, EDIFICIO)
OBSTACULOS = obtener_obstaculos(FILAS, COLUMNAS, matriz, STAR, OBJETIVO)
for obstaculo in OBSTACULOS:
    matriz[obstaculo[0]][obstaculo[1]] = 1

camino = a_estrella(STAR, OBJETIVO, FILAS, COLUMNAS, matriz)
if camino is None:
    print("No se encontró un camino desde el punto de inicio al objetivo.")
else:
    visualizar(FILAS, COLUMNAS, OBJETIVO, STAR, matriz, camino)

