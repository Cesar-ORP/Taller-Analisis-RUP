"""Componente RankingService: implementa CU-R01 Consultar ranking
y CU-R02 Consultar estadísticas de personaje.

Requisitos que implementa: RF-R01, RF-R02, RF-R03, RF-R04, RF-R05.
"""
from typing import List, Optional

from .modelo import CLASES_VALIDAS, EntradaRanking
from .repositorio import EstadisticaRepository

TOP_POR_DEFECTO = 10


class RankingService:
    def __init__(self, repositorio: EstadisticaRepository):
        self._repo = repositorio

    def calcular_ranking(self, clase: Optional[str] = None,
                         top: int = TOP_POR_DEFECTO) -> List[EntradaRanking]:
        """Devuelve el ranking ordenado (RF-R01).

        Orden: puntaje desc -> victorias desc -> derrotas asc -> nombre asc.
        Solo entran personajes con al menos 1 combate (RF-R01).
        clase filtra por Guerrero/Mago/Arquero (RF-R03).
        top limita el tamaño de la lista (RF-R05).
        """
        if clase is not None and clase not in CLASES_VALIDAS:
            raise ValueError(f"Clase inválida: {clase}")
        if top < 1:
            raise ValueError("top debe ser >= 1")

        filas = [
            (p, e) for p, e in self._repo.listar_con_personaje()
            if e.combates_jugados > 0 and (clase is None or p.clase == clase)
        ]
        filas.sort(key=lambda pe: (-pe[1].puntaje, -pe[1].victorias,
                                   pe[1].derrotas, pe[0].nombre.lower()))
        return [EntradaRanking(i, p, e) for i, (p, e) in enumerate(filas[:top], start=1)]

    def consultar_estadisticas(self, id_personaje: int) -> dict:
        """CU-R02 / RF-R04: resumen de estadísticas de un personaje."""
        for p, e in self._repo.listar_con_personaje():
            if p.id_personaje == id_personaje:
                return {
                    "nombre": p.nombre,
                    "clase": p.clase,
                    "combates_jugados": e.combates_jugados,
                    "victorias": e.victorias,
                    "derrotas": e.derrotas,
                    "empates": e.empates,
                    "puntaje": e.puntaje,
                    "porcentaje_victorias": e.porcentaje_victorias,
                }
        raise LookupError(f"Personaje {id_personaje} no existe")  # flujo alterno A2
