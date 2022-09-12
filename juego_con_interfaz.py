from interfaz import jugar_con_interfaz
from clases import Jugador
from tablero import TableroCatan
from juego import rellenar_tablero

Buti = Jugador("Buti", [200, 10, 140])
Seba = Jugador("Seba", [255, 0, 0])

#Lista de jugadores
jugadores = [Seba, Buti]
#Tablero
tablero_a_jugar = TableroCatan()

rellenar_tablero(tablero_a_jugar)

#No se olviden de rellenar el tablero!
jugar_con_interfaz(jugadores,tablero_a_jugar)