ORDEN_ESPECIAL = False
import random as ran
import math
from clases import Asentamiento, Camino, Jugador
from tablero import TableroCatan
import sys

#-----------------------------  UTILS -------------------------------#

def fastRandomInteger(min, max):
    return math.floor((max - min) * ran.random()) - min

def createRandomPopulatedList(table):
    # resourceTable = {
    #    "Ladrillo": 3,
    #    "Trigo"   : 4,
    #    "Madera"  : 4,
    #    "Piedra"  : 3,
    #    "Lana"    : 4
    # }

    # Create a list with all the resources
    order = []
    for item, quantity in table.items():
        for i in range(quantity):
            order.append(item)
    print(order)
    # Shuffle the list
    ran.shuffle(order)

    return order

def tirar_dados():
    dado1 = fastRandomInteger(0, 6) + 1
    dado2 = fastRandomInteger(0, 6) + 1
    return dado1 + dado2

def rellenar_tablero(Tablero: TableroCatan):
    # Create a list with all the resources
    resourceOrder = createRandomPopulatedList({
        "Ladrillo": 3,
        "Piedra"  : 3,
        "Trigo"   : 4,
        "Lana"    : 4,
        "Madera"  : 4
    })

    # Create a list with all the numbers
    numberOrder = createRandomPopulatedList({
        2: 1,
        3: 2,
        4: 2,
        5: 2,
        6: 2,
        8: 2,
        9: 2,
        10: 2,
        11: 2,
        12: 1
    })

    for i in range(19):
        if (i + 1 == 10): continue
        Tablero.colocar_recurso_y_numero(i + 1, resourceOrder.pop(), numberOrder.pop())
    pass

def jugar_catan(jugadores,tablero):
    # Inicio del juego
    inicio_juego(jugadores, tablero)

    for x in range(10):
        print()
        print()
        print("Ronda :" + str(x + 1))
        print('v------------------------------------v')

        for jugador in jugadores:
            if turno_jugador(jugador, tablero) == 'end':
                return
            

        print('^------------------------------------^')
        print("Fin de ronda")

    pass

def turno_jugador(jugador, tablero):

    print()
    print("Turno de " + jugador.nombre)
    print('v-----------------------------v')
    print()

    valorDados = tirar_dados()
    print("Dados: " + str(valorDados))
    if valorDados == 7: return

    
    for i in range(19):
        if (i + 1 == 10): continue
        if tablero.obtener_numero_de_ficha(i + 1) == valorDados:
            for asentamiento in tablero.asentamientos_por_ficha(i + 1):
                asentamiento.dar_recursos(tablero.obtener_recurso_de_ficha(i + 1))

    print()
    print("Recursos:")
    for recurso, cantidad in jugador.recursos.items():
        print(recurso + ": " + str(cantidad))

    while True:
        print()
        comando = input("Comando: ")
        comandoCortado = comando.split(' ')

        match comandoCortado[0]:
            case 'fin':
                return 'end'
            case "pas":
                print("Pasando turno")
                break
            case "ase":
                if (jugador.cantidad_de("Ladrillo") >= 1 
                    and jugador.cantidad_de("Madera") >= 1
                    and jugador.cantidad_de("Trigo") >= 1
                    and jugador.cantidad_de("Lana") >= 1): 

                    jugador.restar_recursos({
                        "Ladrillo": 1,
                        "Madera"  : 1,
                        "Trigo"   : 1,
                        "Lana"    : 1
                    })
                    asentamiento = Asentamiento(jugador)
                    tablero.colocar_asentamiento(int(comandoCortado[1]), int(comandoCortado[2]), asentamiento)
                    print("Asentamiento colocado")
                else:
                    print("No tienes suficientes recursos")
            case "cam":
                if (jugador.cantidad_de("Ladrillo") >= 1 
                    and jugador.cantidad_de("Madera") >= 1): 

                    jugador.restar_recursos({
                        "Ladrillo": 1,
                        "Madera"  : 1
                    })
                    camino = Camino(jugador)
                    tablero.colocar_camino(int(comandoCortado[1]), int(comandoCortado[2]), camino)
                    print("Camino colocado")
                else:
                    print("No tienes suficientes recursos")

    print('^-----------------------------^')
    print("Fin de turno")

    return 'continue'

def inicio_juego(jugadores, tablero):
    for jugador in jugadores:
        print()
        print()
        print("Turno inicial de " + jugador.nombre)
        print('v-----------------------------v')
        for i in range(2):
            asentamiento = Asentamiento(jugador)
            camino = Camino(jugador)

            asentamientoPos = list(map(int, input("Colocar asentamiento: ").split()))
            caminoPos = list(map(int, input("Colocar camino: ").split()))

            tablero.colocar_asentamiento(asentamientoPos[0], asentamientoPos[1], asentamiento)
            tablero.colocar_camino(caminoPos[0], caminoPos[1], camino)
        print('^----------------------------^')
        print("Fin de turno")
    return

Buti = Jugador("Buti", [200, 10, 140])
Seba = Jugador("Seba", [255, 0, 0])

#Lista de jugadores
jugadores = [Seba, Buti]
#Tablero
tablero_a_jugar = TableroCatan()

rellenar_tablero(tablero_a_jugar)

#jugar_catan(jugadores, tablero_a_jugar)

