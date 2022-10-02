ORDEN_ESPECIAL = True
from logging.config import valid_ident
import random as ran
import math
import resource
from typing import List
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
    #print(order)
    # Shuffle the list
    ran.shuffle(order)

    return order

def tirar_dados():
    dado1 = fastRandomInteger(0, 6) + 1
    dado2 = fastRandomInteger(0, 6) + 1
    return dado1 + dado2

def rellenar_tablero(tablero : TableroCatan):
        # Create a list with all the numbers
    numberOrder = [2, 3, 3, 4, 4, 5, 5, 9, 9, 10, 10, 11, 11, 12]
    ran.shuffle(numberOrder)

    sixEightOrder = [6, 6, 8, 8]
    ran.shuffle(sixEightOrder)

    resourceOrder = [
        "Piedra", "Piedra", "Piedra",
        "Ladrillo", "Ladrillo", "Ladrillo",
        "Trigo", "Trigo", "Trigo", "Trigo",
        "Madera", "Madera", "Madera", "Madera",
        "Lana", "Lana", "Lana", "Lana"
    ]
    ran.shuffle(resourceOrder)

    hexagonArray = [
        [None, None, None, None, None, None, None],
    [None, None, 0, 0, 0, None, None],
        [None, 0, 0, 0, 0, None, None],
      [None, 0, 0, 0, 0, 0, None],
        [None, 0, 0, 0, 0, None, None],
    [None, None, 0, 0, 0, None, None],
        [None, None, None, None, None, None, None]
    ]
    spaceCoordinates = {
        1: [1, 2],  2: [1, 3],
        3: [1, 4],  4: [2, 1],
        5: [2, 2],  6: [2, 3],
        7: [2, 4],  8: [3, 1],
        9: [3, 2],  10: [3, 3],
        11: [3, 4], 12: [3, 5],
        13: [4, 1], 14: [4, 2],
        15: [4, 3], 16: [4, 4],
        17: [5, 2], 18: [5, 3],
        19: [5, 4],
    }

    placeEverySixOrEight(hexagonArray, tablero, spaceCoordinates, sixEightOrder, resourceOrder)

    for hexa in range(1, 20):
        if hexagonArray[spaceCoordinates[hexa][0]][spaceCoordinates[hexa][1]] != 0 or hexa == 10: continue
        num = numberOrder.pop()
        tablero.colocar_recurso_y_numero(hexa, resourceOrder.pop(), num)
        hexagonArray[spaceCoordinates[hexa][0]][spaceCoordinates[hexa][1]] = num
    pass


def hasAdjecentSixOrEight(hexagonArray, currentHexagonY, currentHexagonX):
    startX = 0
    endX = 0
    for adjacentY in range(currentHexagonY - 1, currentHexagonY + 2):

        if adjacentY != currentHexagonY:
            if currentHexagonY % 2 == 0:
                startX = currentHexagonX
                endX = currentHexagonX + 1
            else:
                startX = currentHexagonX - 1
                endX = currentHexagonX
        else:
            startX = currentHexagonX - 1
            endX = currentHexagonX + 1

        for adjacentX in range(startX, endX + 1):
            if adjacentX == currentHexagonX and adjacentY == currentHexagonY: continue

            if hexagonArray[adjacentY][adjacentX] in [6, 8]:
                return True
    return False

def placeEverySixOrEight(hexagonArray, tablero, hexCoordinates, sixEightOrder, resourceOrder):

    while sixEightOrder:

        nextHexagonToPlace = fastRandomInteger(0, 19) + 1
        if hexagonArray[hexCoordinates[nextHexagonToPlace][0]][hexCoordinates[nextHexagonToPlace][1]] != 0 or nextHexagonToPlace == 10: continue
        for hexagonLine in hexagonArray:
            print(hexagonLine)
        
        if not hasAdjecentSixOrEight(hexagonArray, hexCoordinates[nextHexagonToPlace][0], hexCoordinates[nextHexagonToPlace][1]):
            num = sixEightOrder.pop()
            tablero.colocar_recurso_y_numero(nextHexagonToPlace, resourceOrder.pop(), num)
            hexagonArray[hexCoordinates[nextHexagonToPlace][0]][hexCoordinates[nextHexagonToPlace][1]] = num

def jugar_catan(jugadores,tablero):
    # Inicio del juego
    inicio_juego(jugadores, tablero)

    for x in range(10):
        print()
        print()
        print("Ronda :" + str(x + 1))
        print('v------------------------------------v')

        for jugador in jugadores:
            if jugar_turno(jugador, tablero) == 'end':
                return
            

        print('^------------------------------------^')
        print("Fin de ronda")

    pass

def jugar_turno(jugador, tablero):

    print("\nTurno de " + jugador.nombre)
    print('v-----------------------------v\n')

    valorDados = tirar_dados()
    print("Dados: " + str(valorDados))
    if valorDados == 7: return

    
    for i in range(19):
        if (i + 1 == 10): continue
        if tablero.obtener_numero_de_ficha(i + 1) == valorDados:
            for asentamiento in tablero.asentamientos_por_ficha(i + 1):
                asentamiento.dar_recursos(tablero.obtener_recurso_de_ficha(i + 1))

    print("\nRecursos:")
    for recurso, cantidad in jugador.recursos.items():
        print(recurso + ": " + str(cantidad))

    while True:
        comando = input("\nComando: ")
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

def inicio_juego(jugadores, tablero: TableroCatan):

    for jugador in jugadores:
        print("\n\nPrimer turno inicial de " + jugador.nombre)
        print('v-----------------------------v')

        asentamiento = Asentamiento(jugador)
        camino = Camino(jugador)

        asentamientoPos = list(map(int, input("Colocar asentamiento: ").split()))
        tablero.colocar_asentamiento(asentamientoPos[0], asentamientoPos[1], asentamiento)

        giveInitialResources(tablero, asentamientoPos, asentamiento)

        caminoPos = list(map(int, input("Colocar camino: ").split()))
        tablero.colocar_camino(caminoPos[0], caminoPos[1], camino)
        print('^----------------------------^')
        print("Fin de turno")

    for jugador in list(reversed(jugadores)):

        print("\n\nSegundo turno inicial de " + jugador.nombre)
        print('v-----------------------------v')
        
        asentamiento = Asentamiento(jugador)
        camino = Camino(jugador)

        asentamientoPos = list(map(int, input("Colocar asentamiento: ").split()))
        tablero.colocar_asentamiento(asentamientoPos[0], asentamientoPos[1], asentamiento)

        giveInitialResources(tablero, asentamientoPos, asentamiento)


        caminoPos = list(map(int, input("Colocar camino: ").split()))
        tablero.colocar_camino(caminoPos[0], caminoPos[1], camino)
        print('^----------------------------^')
        print("Fin de turno")

    return

def giveInitialResources(tablero: TableroCatan, asentamientoPos, asentamiento):
    
    spaceCoordinates = {
        1: [1, 2],  2: [1, 3],
        3: [1, 4],  4: [2, 1],
        5: [2, 2],  6: [2, 3],
        7: [2, 4],  8: [3, 1],
        9: [3, 2],  10: [3, 3],
        11: [3, 4], 12: [3, 5],
        13: [4, 1], 14: [4, 2],
        15: [4, 3], 16: [4, 4],
        17: [5, 2], 18: [5, 3],
        19: [5, 4],
    }

    fichaAse = asentamientoPos[0]
    asentamiento.dar_recursos(tablero.obtener_recurso_de_ficha(fichaAse))
    aristaAse = asentamientoPos[1]

    adjacentSpacesCoordinates = getAdjacentCoordinatesTo(spaceCoordinates[fichaAse])
    spaces = []

    #Posicion 1 de la posicion adjacente a la arista
    spaces.append([adjacentSpacesCoordinates[aristaAse - 1][0], adjacentSpacesCoordinates[aristaAse - 1][1]])

    #Posicion 2 de la posicion adjacente a la arista
    if aristaAse != 6: 
        spaces.append([adjacentSpacesCoordinates[aristaAse][0], adjacentSpacesCoordinates[aristaAse][1]])
    else:
        spaces.append([adjacentSpacesCoordinates[0][0], adjacentSpacesCoordinates[0][1]])

    keyList = list(spaceCoordinates.keys())
    valList = list(spaceCoordinates.values())
    for fichaPos in spaces:
        if fichaPos in valList:
            ficha = keyList[valList.index(fichaPos)]
            asentamiento.dar_recursos(tablero.obtener_recurso_de_ficha(ficha))

    return

def getAdjacentCoordinatesTo(space):
    additive = 0
    if space[0] % 2 == 0:
        additive = 1

    return [
        [space[0] - 1, space[1] -  1 + additive],
        [space[0] - 1, space[1] + additive],
        [space[0] + 0, space[1] +  1],
        [space[0] + 1, space[1] + additive],
        [space[0] + 1, space[1] -  1 + additive],
        [space[0] + 0, space[1] -  1]
    ]



    