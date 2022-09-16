ORDEN_ESPECIAL = True
import random as ran
import math
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

def rellenar_tablero(tablero: TableroCatan):
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

    hexagonArray = [
    [None, None, None, None, None, None, None],
    [None, None, 0, 0, 0, None, None],
    [None, 0, 0, 0, 0, None, None],
    [None, 0, 0, 0, 0, 0, None],
    [None, 0, 0, 0, 0, None, None],
    [None, None, 0, 0, 0, None, None],
    [None, None, None, None, None, None, None]
    ]

    currentHexagon = 1

    for currentHexagonY, hexagonLine in enumerate(hexagonArray):
        for currentHexagonX, hexagonValue in enumerate(hexagonLine):
            if currentHexagon in [10, 20]: break
            if hexagonValue == None: continue
            #Inside the hexagon line and a valid spot

            #If the next one is not a 6 or 8
            if numberOrder[-1] not in [6, 8]:
                num = numberOrder.pop()
                tablero.colocar_recurso_y_numero(currentHexagon, resourceOrder.pop(), num)
                hexagonArray[currentHexagonY][currentHexagonX] = num
                currentHexagon += 1
                continue


            #If it is
            for adjacentY in range(currentHexagonY - 1, currentHexagon + 2):
                for adjacentX in range(currentHexagonX - 1, currentHexagon + 2):
                    if adjacentX == currentHexagonX and adjacentY == currentHexagonY: continue

                    if hexagonValue in [6, 8]:
                        while numberOrder[-1] in [6, 8]:
                            numberOrder.insert(0, numberOrder.pop())
                        num = numberOrder.pop()
                        tablero.colocar_recurso_y_numero(currentHexagon, resourceOrder.pop(), num)
                        hexagonArray[currentHexagonY][currentHexagonX] = num
                        break
                else: continue #On completion of the inner loop
                break #If inner loop is broken, break the outer loop
            
            currentHexagon += 1
        else: continue #On completion of the inner loop
        break #If inner loop is broken, break the outer loop
    print(hexagonArray)
    # hexagonCount = 19

    # for hexagonIndex in range(hexagonCount):
    #     if (hexagonIndex + 1 == 10): continue
    #     tablero.colocar_recurso_y_numero(hexagonIndex + 1, resourceOrder.pop(), numberOrder.pop())
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

def inicio_juego(jugadores, tablero):
    for jugador in jugadores:
        print("\n\nPrimer turno inicial de " + jugador.nombre)
        print('v-----------------------------v')

        asentamiento = Asentamiento(jugador)
        camino = Camino(jugador)

        asentamientoPos = list(map(int, input("Colocar asentamiento: ").split()))
        caminoPos = list(map(int, input("Colocar camino: ").split()))

        tablero.colocar_asentamiento(asentamientoPos[0], asentamientoPos[1], asentamiento)
        tablero.colocar_camino(caminoPos[0], caminoPos[1], camino)
        print('^----------------------------^')
        print("Fin de turno")

    for jugador in list(reversed(jugadores)):

        print("\n\nSegundo turno inicial de " + jugador.nombre)
        print('v-----------------------------v')
        
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
#print(tablero_a_jugar.obtener_arista(10, 5))

#jugar_catan(jugadores, tablero_a_jugar)

# def rellenar_tablero_debug():
#     # Create a list with all the numbers
#     numberOrder = [5,3,4,4,10,3,9,12,2,9,11,5,11,10]

#     hexagonArray = [
#     [None, None, None, None, None, None, None],
#     [None, None, 0, 0, 0, None, None],
#     [None, 0, 0, 0, 0, None, None],
#     [None, 0, 0, 0, 0, 0, None],
#     [None, 0, 0, 0, 0, None, None],
#     [None, None, 0, 0, 0, None, None],
#     [None, None, None, None, None, None, None]
#     ]

#     currentHexagon = 1

#     sixEightOrder = [6, 6 ,8 ,8]

#     placeEverySixOrEight(hexagonArray, sixEightOrder)

#     for currentHexagonY, hexagonLine in enumerate(hexagonArray):
#         for currentHexagonX, hexagonValue in enumerate(hexagonLine):
#             if hexagonValue == None: continue
#             if currentHexagon == 20: break

#             if currentHexagon == 10 or hexagonValue != 0: 
#                 currentHexagon += 1 
#                 continue
#             #Inside the hexagon line and a valid spot

#             #If the next one is not a 6 or 8
#             # if numberOrder[-1] not in [6, 8]:
#             #     num = numberOrder.pop()
#             #     hexagonArray[currentHexagonY][currentHexagonX] = num
#             #     currentHexagon += 1
#             #     continue

#             num = numberOrder.pop()
#             hexagonArray[currentHexagonY][currentHexagonX] = num
#             #If it is
#             # for adjacentY in range(currentHexagonY - 1, currentHexagonY + 1):
#             #     for adjacentX in range(currentHexagonX - 1, currentHexagonX + 1):
#             #         if adjacentX == currentHexagonX and adjacentY == currentHexagonY: continue

#             #         if hexagonArray[adjacentY][adjacentX] in [6, 8]:
#             #             while numberOrder[-1] in [6, 8]:
#             #                 cache.append(numberOrder.pop())
#             #             num = numberOrder.pop()
#             #             hexagonArray[currentHexagonY][currentHexagonX] = num
#             #             for cacheSpace in range(len(cache)):
#             #                 numberOrder.append(cache.pop())
#             #             break
#             #     else: 
#             #         continue #If there was no 6, 8, go to next line

#             #     break #If there was a 6, 8, break the ENTIRE loop

#             # else: #If there was no 6, 8 in every line, put the 6 or 8 in the hexagon
#             #     num = numberOrder.pop()
#             #     hexagonArray[currentHexagonY][currentHexagonX] = num
            
#             currentHexagon += 1

#         else: 
#             continue #On completion of the inner loop, go to next line

#         break #If there was an exception, break the entire loop
#     pass

def rellenar_tablero_debug2():
        # Create a list with all the numbers
    numberOrder = [5,3,4,4,10,3,9,12,2,9,11,5,11,10]
    sixEightOrder = [6, 6 ,8 ,8]

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

    placeEverySixOrEight(hexagonArray, spaceCoordinates, sixEightOrder)

    for hexa in range(1, 20):
        if hexagonArray[spaceCoordinates[hexa][0]][spaceCoordinates[hexa][1]] != 0 or hexa == 10: continue
        num = numberOrder.pop()
        hexagonArray[spaceCoordinates[hexa][0]][spaceCoordinates[hexa][1]] = num
    pass


def hasAdjecentSixOrEight(hexagonArray, currentHexagonY, currentHexagonX):
    for adjacentY in range(currentHexagonY - 1, currentHexagonY + 1):
        for adjacentX in range(currentHexagonX - 1, currentHexagonX + 1):
            if adjacentX == currentHexagonX and adjacentY == currentHexagonY: continue

            if hexagonArray[adjacentY][adjacentX] in [6, 8]:
                return True
    return False

def placeEverySixOrEight(hexagonArray, hexCoordinates, sixEightOrder):

    while sixEightOrder:

        nextHexagonToPlace = fastRandomInteger(0, 19) + 1
        if hexagonArray[hexCoordinates[nextHexagonToPlace][0]][hexCoordinates[nextHexagonToPlace][1]] != 0: continue
        
        if not hasAdjecentSixOrEight(hexagonArray, hexCoordinates[nextHexagonToPlace][0], hexCoordinates[nextHexagonToPlace][1]):

            hexagonArray[hexCoordinates[nextHexagonToPlace][0]][hexCoordinates[nextHexagonToPlace][1]] = sixEightOrder.pop()

rellenar_tablero_debug()

