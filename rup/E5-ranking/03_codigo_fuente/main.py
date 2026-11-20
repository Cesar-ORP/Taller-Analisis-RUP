"""Componente ConsolaRanking: interfaz mínima para ejecutar el ranking.

Uso:
    python main.py              # top 10 general
    python main.py Mago         # top 10 solo Magos
    python main.py Guerrero 3   # top 3 de Guerreros
"""
import sys

from ranking import Estadistica, EstadisticaRepositoryMemoria, Personaje, RankingService

DATOS_DEMO = [
    # (id, jugador, nombre, clase, nivel, victorias, derrotas, empates)
    (1, 1, "Torvak", "Guerrero", 12, 8, 2, 1),
    (2, 1, "Eldrin", "Mago", 15, 9, 1, 0),
    (3, 2, "Sylva", "Arquero", 11, 8, 1, 1),
    (4, 2, "Merlina", "Mago", 7, 3, 5, 2),
    (5, 3, "Brena", "Guerrero", 9, 8, 3, 1),
    (6, 3, "Robin", "Arquero", 4, 1, 4, 0),
    (7, 4, "Novato", "Mago", 1, 0, 0, 0),  # sin combates: no aparece
]


def cargar_demo() -> EstadisticaRepositoryMemoria:
    repo = EstadisticaRepositoryMemoria()
    for idp, idj, nombre, clase, nivel, v, d, e in DATOS_DEMO:
        repo.guardar(Personaje(idp, idj, nombre, clase, nivel), Estadistica(idp, v, d, e))
    return repo


def main(argv):
    clase = argv[1] if len(argv) > 1 else None
    top = int(argv[2]) if len(argv) > 2 else 10
    servicio = RankingService(cargar_demo())
    titulo = f"RANKING {clase.upper()}" if clase else "RANKING GENERAL"
    print(f"=== {titulo} (top {top}) ===")
    print(f"{'#':>2}  {'Personaje':<10} {'Clase':<9} {'V':>3} {'D':>3} {'E':>3} {'Pts':>4}")
    for fila in servicio.calcular_ranking(clase, top):
        e = fila.estadistica
        print(f"{fila.posicion:>2}  {fila.personaje.nombre:<10} {fila.personaje.clase:<9} "
              f"{e.victorias:>3} {e.derrotas:>3} {e.empates:>3} {fila.puntaje:>4}")


if __name__ == "__main__":
    main(sys.argv)
