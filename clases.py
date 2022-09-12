import pygame
import math
import random as ran
from tablero import TableroCatan


class Asentamiento:
    def __init__(self, jugador):
        self.jugador = jugador

    def dar_recursos(self, recurso):
        self.jugador.recursos[recurso] += 1

    pass

class Ciudad:
    pass

class Camino:
    def __init__(self, jugador):
        self.jugador = jugador
    
    pass

class Jugador:
    def __init__(self, nombre, color):
        self.nombre = nombre
        self.color = color
        self.recursos = {
            "Ladrillo": 0,
            "Trigo"   : 0,
            "Madera"  : 0,
            "Piedra"  : 0,
            "Lana"    : 0
        }
    
    def cantidad_de(self, recurso):
        return self.recursos[recurso]

    def restar_recursos(self, recursos):
        for recurso, quantity in recursos.items():
            self.recursos[recurso] -= quantity

    pass


#---------------------------- UTILS ----------------------------#


#---------------------------- DEBUG ----------------------------#

