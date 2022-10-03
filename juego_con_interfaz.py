from interfaz import jugar_con_interfaz
from clases import Jugador
from tablero import TableroCatan
from juego import rellenar_tablero

"""
Para correr el juego, simplemente correr este archivo
Para utilizar los extras, cambiar las variables dentro de juego.py, las variables son las siguientes:
    
    ORDEN_ESPECIAL: True para usar el orden especial de inicio, False para usar el orden normal inicial
    RELLENAR_MEJORADO: True para usar el rellenado mejorado, False para usar el rellenado basico
    RECURSOS_INICIALES: True para usar los recursos iniciales, False para no usarlos

Hecho por Sebastian Loucim, Agustin Butierrez y Marco Palazzo
"""

def main():
    Buti = Jugador("Buti", [200, 10, 140])
    Seba = Jugador("Seba", [255, 0, 0])

    #Lista de jugadores
    jugadores = [Seba, Buti]
    #Tablero
    tablero_a_jugar = TableroCatan()

    #No se olviden de rellenar el tablero!
    rellenar_tablero(tablero_a_jugar)
    
    jugar_con_interfaz(jugadores,tablero_a_jugar)

if __name__ == "__main__":
    main()
