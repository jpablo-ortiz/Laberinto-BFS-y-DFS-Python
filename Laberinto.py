# Imports

# import sys

# Constantes

DIRECTORIO_DE_PROYECTO = "D:\Juanpa\Programacion\Python\CS50_Introduction_to_Artificial_Intelligence_with_Python_Certificación_Harvard\Search\Recursos y hechos por mi\Laberinto (BFS y DFS)"
DIRECTORIO_LABERINTOS = "D:\Juanpa\Programacion\Python\CS50_Introduction_to_Artificial_Intelligence_with_Python_Certificación_Harvard\Search\Recursos y hechos por mi\Laberinto (BFS y DFS)\src0"

# Clases


class Nodo():
    def __init__(self, padre, estado, accion):
        self.padre = padre
        self.estado = estado
        self.accion = accion


class FronteraPila():
    def __init__(self):
        self.frontera = []

    def agregar(self, nodo):
        self.frontera.append(nodo)

    def estaVacia(self):
        return len(self.frontera) == 0

    def eliminar(self):
        if self.estaVacia():
            raise("Frontera Vacía")
        else:
            nodo = self.frontera[-1]
            self.frontera = self.frontera[:-1]
            return nodo


    def contieneEstado(self, estado):
        return any(nodo.estado == estado for nodo in self.frontera)


class FronteraCola(FronteraPila):
    def eliminar(self):
        if self.estaVacia():
            raise("Frontera Vacía")
        else:
            nodo = self.frontera[0]
            self.frontera = self.frontera[1:]
            return nodo


class Laberinto():
    def __init__(self, nombreDelArchivo, tipoBusqueda):
        self.tipoBusqueda = tipoBusqueda

        # Leer el arcivo del laberinto
        with open(nombreDelArchivo) as f:
            contenido = f.read()

        # Validar el estado inicio y meta
        if contenido.count("A") != 1:
            raise("Debe existir exactamente una A en el laberinto (.txt)")
        if contenido.count("B") != 1:
            raise("Debe existir exactamente una B en el laberinto (.txt)")

        # Determinar el alto y ancho del laberinto
        contenido = contenido.splitlines()
        self.alto = len(contenido)
        self.ancho = max(len(fila) for fila in contenido)

        # Keep track of walls
        self.muros = []
        for i in range(self.alto):
            fila = []
            for j in range(self.ancho):
                try:
                    if contenido[i][j] == " ":
                        fila.append(False)
                    elif contenido[i][j] == "A":
                        fila.append(False)
                        self.inicio = (i, j)
                    elif contenido[i][j] == "B":
                        fila.append(False)
                        self.meta = (i, j)
                    else:
                        fila.append(True)
                except IndexError:
                    fila.append(False)
            self.muros.append(fila)

        # Declarar la solucion
        self.solucion = None

    def imprimir(self):
        # Verificar si se va a mostrar resuelto o no
        solucionEstados = self.solucion[1] if self.solucion is not None else None

        # Dibujar Laberinto
        print()
        for i, fila in enumerate(self.muros):
            for j, columna in enumerate(fila):
                if columna:
                    print("█", end="")
                elif (i, j) == self.inicio:
                    print("A", end="")
                elif (i, j) == self.meta:
                    print("B", end="")
                elif solucionEstados is not None and (i, j) in solucionEstados:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()

    def vecinos(self, estado):
        fila = estado[0]
        columna = estado[1]

        candidatos = [
            ("Arriba",   (fila - 1, columna)),
            ("Abajo",    (fila + 1, columna)),
            ("Izquierda", (fila, columna - 1)),
            ("Derecha",  (fila, columna + 1)),
        ]

        resultado = []
        for accion, (f, c) in candidatos:
            if self.alto > f >= 0 and self.ancho > c >= 0 and not self.muros[f][c]:
                resultado.append((accion, (f, c)))
        return resultado

    def resolver(self):
        # Mantener rastreo del numero de estados explorados
        self.numExplorados = 0

        # Inicializar frontera solo al estado inicio
        inicio = Nodo(padre=None, estado=self.inicio, accion=None)
        if self.tipoBusqueda == 1:
            frontera = FronteraPila()
        else:
            frontera = FronteraCola()
        frontera.agregar(inicio)

        # Inicializar un conjunto vacio de explorados
        self.explorados = set()

        # Mantener ciclo mientras que se encuentra la solución
        while True:

            # Si no hay nada en la frontera entonces no hay trayecto
            if frontera.estaVacia():
                raise("No hay solución para este laberinto")

            # Elegir un nodo de la frontera
            nodo = frontera.eliminar()
            self.numExplorados += 1

            # Marcar nodo como explorado
            self.explorados.add(nodo.estado)

            # Agregar Vecinos a la frontera
            for accion, estado in self.vecinos(nodo.estado):
                if not frontera.contieneEstado(estado) and estado not in self.explorados:
                    hijo = Nodo(padre=nodo, estado=estado, accion=accion)
                    frontera.agregar(hijo)

                    # Si el hijo es la meta, entonces ya tenemos la solucion
                    if hijo.estado == self.meta:
                        acciones = []
                        celdas = []
                        while hijo.padre is not None:
                            acciones.append(hijo.accion)
                            celdas.append(hijo.estado)
                            hijo = hijo.padre
                        acciones.reverse()
                        celdas.reverse()
                        self.solucion = (acciones, celdas)
                        return self.solucion

    def crearArchivoImagen(self, nombreDelArchivo, mostrarSolucion=True, mostrarExploracion=False):
        from PIL import Image, ImageDraw
        tamanioCelda = 50
        tamanioMargen = 2

        # Crear el linezo en blanco (blank canvas)
        image = Image.new(mode="RGBA", size=(self.ancho * tamanioCelda, self.alto * tamanioCelda), color="black")
        draw = ImageDraw.Draw(image)
        
        solucion = self.solucion[1] if self.solucion is not None else None
        for i, fila in enumerate(self.muros):
            for j, columna in enumerate(fila):
                # Walls
                if columna:
                    fill = (40, 40, 40)

                # Start
                elif (i,j) == self.inicio:
                    fill = (255, 0, 0)
 
                # Goal
                elif (i,j) == self.meta:
                    fill = (0, 171, 28)
 
                # Solution
                elif solucion is not None and mostrarSolucion and (i,j) in solucion:
                    fill = (220, 235, 113)

                # Explored
                elif solucion is not None and mostrarExploracion and (i,j) in self.explorados:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(fill=fill, xy=([(j * tamanioCelda + tamanioMargen, i * tamanioCelda + tamanioMargen), ( (j + 1) * tamanioCelda - tamanioMargen, (i + 1) * tamanioCelda - tamanioMargen)]))
        
        image.save(nombreDelArchivo)

def menu():
    i = 0
    while True:
        try:
            i += 1
            directorio = DIRECTORIO_LABERINTOS + "\maze" + str(i) + ".txt"
            with open(directorio) as f:
                contenido = f.read()
                print(str(i) + ") maze" + str(i))
        except Exception as e:
            #print(e)
            break

    res = input("Seleccione un laberinto:")
    directorioLaberinto = DIRECTORIO_LABERINTOS + "\maze" + res + ".txt"

    print()
    print("1) DFS")
    print("2) BFS")
    res = input("Seleccione el modo de exploración")
    return (directorioLaberinto, int(res))

# Main
'''
if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

    m = Laberinto(sys.argv[1])
print("Maze:")
m.imprimir()
print("Solving...")
m.resolver()
print("States Explored:", m.numExplorados)
print("Solution:")
m.imprimir()
m.output_image(DIRECTORIO_DE_PROYECTO + "\maze.png", show_explored=True)
'''

nombreDelArchivo, tipoBusqueda = menu()
m = Laberinto(nombreDelArchivo, tipoBusqueda)
print("Maze:")
m.imprimir()
print("Solving...")
m.resolver()
print("States Explored:", m.numExplorados)
print("Solution:")
m.imprimir()
m.crearArchivoImagen(DIRECTORIO_DE_PROYECTO + "\maze.png", mostrarExploracion=True)
