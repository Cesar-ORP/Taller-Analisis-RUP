"""Componente EstadisticaRepository: acceso a datos del ranking.

En producción lee de MariaDB (vista vista_ranking del script 02_modelo_datos.sql).
Para la iteración C1 se entrega una implementación en memoria que permite
ejecutar y probar el componente sin base de datos.
"""
from typing import Dict, List, Tuple

from .modelo import Estadistica, Personaje


class EstadisticaRepository:
    """Interfaz: lo que RankingService necesita de la capa de datos."""

    def listar_con_personaje(self) -> List[Tuple[Personaje, Estadistica]]:
        raise NotImplementedError


class EstadisticaRepositoryMemoria(EstadisticaRepository):
    def __init__(self):
        self._personajes: Dict[int, Personaje] = {}
        self._estadisticas: Dict[int, Estadistica] = {}

    def guardar(self, personaje: Personaje, estadistica: Estadistica) -> None:
        if personaje.id_personaje != estadistica.id_personaje:
            raise ValueError("La estadística no corresponde al personaje")
        self._personajes[personaje.id_personaje] = personaje
        self._estadisticas[personaje.id_personaje] = estadistica

    def listar_con_personaje(self) -> List[Tuple[Personaje, Estadistica]]:
        return [(self._personajes[i], self._estadisticas[i]) for i in self._personajes]


class EstadisticaRepositoryMariaDB(EstadisticaRepository):
    """Implementación real (requiere: pip install mariadb). Se integra en C2."""

    CONSULTA = (
        "SELECT p.id_personaje, p.id_jugador, p.nombre, p.clase, p.nivel, "
        "e.victorias, e.derrotas, e.empates "
        "FROM personaje p JOIN estadistica e ON e.id_personaje = p.id_personaje"
    )

    def __init__(self, conexion):
        self._conexion = conexion

    def listar_con_personaje(self) -> List[Tuple[Personaje, Estadistica]]:
        cur = self._conexion.cursor()
        cur.execute(self.CONSULTA)
        filas = []
        for idp, idj, nombre, clase, nivel, v, d, e in cur.fetchall():
            filas.append((Personaje(idp, idj, nombre, clase, nivel), Estadistica(idp, v, d, e)))
        return filas
