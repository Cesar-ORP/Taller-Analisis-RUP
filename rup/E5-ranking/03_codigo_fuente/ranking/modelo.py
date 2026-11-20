"""Entidades del módulo Ranking y estadísticas (RPG Manager).

Los nombres coinciden con el modelo de datos (02_modelo_datos.sql):
  tabla personaje   -> clase Personaje
  tabla estadistica -> clase Estadistica
"""
from dataclasses import dataclass

CLASES_VALIDAS = ("Guerrero", "Mago", "Arquero")

PUNTOS_VICTORIA = 3
PUNTOS_EMPATE = 1


@dataclass(frozen=True)
class Personaje:
    id_personaje: int
    id_jugador: int
    nombre: str
    clase: str
    nivel: int = 1

    def __post_init__(self):
        if self.clase not in CLASES_VALIDAS:
            raise ValueError(f"Clase inválida: {self.clase}")


@dataclass(frozen=True)
class Estadistica:
    id_personaje: int
    victorias: int = 0
    derrotas: int = 0
    empates: int = 0

    def __post_init__(self):
        if min(self.victorias, self.derrotas, self.empates) < 0:
            raise ValueError("Las estadísticas no pueden ser negativas")

    @property
    def combates_jugados(self) -> int:
        return self.victorias + self.derrotas + self.empates

    @property
    def puntaje(self) -> int:
        """RF-R02: puntaje = 3 x victorias + 1 x empates."""
        return PUNTOS_VICTORIA * self.victorias + PUNTOS_EMPATE * self.empates

    @property
    def porcentaje_victorias(self) -> float:
        """RF-R04: % de victorias con 1 decimal (0.0 si no ha combatido)."""
        if self.combates_jugados == 0:
            return 0.0
        return round(100 * self.victorias / self.combates_jugados, 1)


@dataclass(frozen=True)
class EntradaRanking:
    posicion: int
    personaje: Personaje
    estadistica: Estadistica

    @property
    def puntaje(self) -> int:
        return self.estadistica.puntaje
