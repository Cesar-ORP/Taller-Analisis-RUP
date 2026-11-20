"""Pruebas unitarias del componente (insumo para el Plan y casos de prueba de E6).

Ejecutar desde 03_codigo_fuente/:  python -m unittest discover -s tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import cargar_demo  # noqa: E402
from ranking import Estadistica, EstadisticaRepositoryMemoria, Personaje, RankingService  # noqa: E402


class TestRanking(unittest.TestCase):
    def setUp(self):
        self.servicio = RankingService(cargar_demo())

    def test_rf_r01_orden_por_puntaje_descendente(self):
        nombres = [f.personaje.nombre for f in self.servicio.calcular_ranking()]
        self.assertEqual(nombres, ["Eldrin", "Sylva", "Torvak", "Brena", "Merlina", "Robin"])

    def test_rf_r01_excluye_personajes_sin_combates(self):
        nombres = [f.personaje.nombre for f in self.servicio.calcular_ranking()]
        self.assertNotIn("Novato", nombres)

    def test_rf_r02_formula_de_puntaje(self):
        self.assertEqual(Estadistica(1, victorias=8, derrotas=2, empates=1).puntaje, 25)

    def test_desempate_por_menos_derrotas(self):
        # Sylva 25 pts (8V 1D) y Torvak 25 pts (8V 2D): gana quien tiene menos derrotas
        ranking = self.servicio.calcular_ranking()
        self.assertEqual((ranking[1].personaje.nombre, ranking[1].puntaje), ("Sylva", 25))
        self.assertEqual((ranking[2].personaje.nombre, ranking[2].puntaje), ("Torvak", 25))

    def test_desempate_final_por_nombre(self):
        repo = EstadisticaRepositoryMemoria()
        repo.guardar(Personaje(1, 1, "Zeta", "Mago"), Estadistica(1, 2, 1, 0))
        repo.guardar(Personaje(2, 1, "Alfa", "Mago"), Estadistica(2, 2, 1, 0))
        nombres = [f.personaje.nombre for f in RankingService(repo).calcular_ranking()]
        self.assertEqual(nombres, ["Alfa", "Zeta"])

    def test_rf_r03_filtro_por_clase(self):
        ranking = self.servicio.calcular_ranking(clase="Mago")
        self.assertEqual([f.personaje.nombre for f in ranking], ["Eldrin", "Merlina"])
        self.assertEqual([f.posicion for f in ranking], [1, 2])

    def test_rf_r03_clase_invalida(self):
        with self.assertRaises(ValueError):
            self.servicio.calcular_ranking(clase="Paladin")

    def test_rf_r05_top_n(self):
        self.assertEqual(len(self.servicio.calcular_ranking(top=3)), 3)

    def test_top_invalido(self):
        with self.assertRaises(ValueError):
            self.servicio.calcular_ranking(top=0)

    def test_rf_r04_estadisticas_de_personaje(self):
        datos = self.servicio.consultar_estadisticas(1)
        self.assertEqual(datos["combates_jugados"], 11)
        self.assertEqual(datos["porcentaje_victorias"], 72.7)

    def test_rf_r04_personaje_sin_combates(self):
        self.assertEqual(self.servicio.consultar_estadisticas(7)["porcentaje_victorias"], 0.0)

    def test_cu_r02_a2_personaje_inexistente(self):
        with self.assertRaises(LookupError):
            self.servicio.consultar_estadisticas(999)

    def test_ranking_vacio(self):
        self.assertEqual(RankingService(EstadisticaRepositoryMemoria()).calcular_ranking(), [])


if __name__ == "__main__":
    unittest.main()
