# 00 · Eslabón de trazabilidad — E5 Construcción (Ranking y estadísticas)

**Dueño:** David Alejandro Villamil

Como E4 trabajó el módulo Misiones, no recibimos su diseño del Ranking. Por eso escribimos aquí una versión **mínima** de los insumos que necesitamos. *En un proyecto real, esto lo producirían el Especificador de requisitos (E2) y el Arquitecto/Diseñador (E4).*

## 1. Lo que recibimos (insumo mínimo, hecho por nosotros)

### 1.1 Requisitos (lo produciría el Especificador de requisitos — E2)
| ID | Requisito | Verificable con |
|---|---|---|
| RF-R01 | El sistema muestra el ranking ordenado por puntaje descendente; solo aparecen personajes con al menos 1 combate. | Datos de ejemplo → orden esperado |
| RF-R02 | Puntaje = 3 × victorias + 1 × empates. | 8V, 2D, 1E → 25 pts |
| RF-R03 | El jugador puede filtrar el ranking por clase (Guerrero, Mago, Arquero). | Filtro Mago → solo Magos |
| RF-R04 | El jugador puede ver combates, V/D/E y % de victorias de un personaje. | 8V de 11 → 72,7 % |
| RF-R05 | El ranking muestra el top 10 por defecto; el jugador puede pedir otro N. | top=3 → 3 filas |
| RNF-R01 | El ranking de 10.000 personajes se genera en menos de 2 s. | Prueba de carga (C2) |

### 1.2 Caso de uso en 5 líneas (lo produciría el Especificador de requisitos — E2)
**CU-R01 Consultar ranking** · Actor: Jugador
1. El jugador abre la opción *Ranking*.
2. El sistema muestra el top 10 general ordenado por puntaje (RF-R01, RF-R02, RF-R05).
3. El jugador elige una clase; el sistema muestra el ranking solo de esa clase (RF-R03).
4. **A1:** si no hay personajes con combates, el sistema muestra "Aún no hay combates registrados".
5. **A2:** si la clase no existe, el sistema muestra "Clase inválida" y conserva el ranking general.

### 1.3 Diagrama de clases de diseño mínimo (lo produciría el Diseñador — E4)
```
RankingService
  + calcular_ranking(clase: str = None, top: int = 10) : List<EntradaRanking>
  + consultar_estadisticas(id_personaje: int) : dict
  - repositorio : EstadisticaRepository
EstadisticaRepository
  + listar_con_personaje() : List<(Personaje, Estadistica)>
Personaje   { id_personaje, id_jugador, nombre, clase, nivel }
Estadistica { id_personaje, victorias, derrotas, empates, /combates_jugados, /puntaje }
EntradaRanking { posicion, personaje, estadistica }
```
### 1.4 Del Modelo del dominio (lo produciría E3)
Conceptos que usamos: **Jugador** *tiene* **Personaje**; **Personaje** *participa en* **Combate**; **Combate** *produce* resultado (victoria / derrota / empate) que se acumula en **Estadística**.

## 2. Lo que nosotros producimos (E5)
| Artefacto | Archivo |
|---|---|
| 14 Plan de iteración | `01_plan_iteracion.md` |
| 15 Modelo de datos | `02_modelo_datos.puml`, `02_modelo_datos.png`, `02_modelo_datos.sql` |
| 16 Código fuente y componentes | `03_codigo_fuente/` (código, pruebas, README, diagrama de componentes) |

## 3. A qué alimentamos (fase siguiente — E6 Pruebas y transición)
| Producimos | Alimenta a | Cómo |
|---|---|---|
| Código + pruebas unitarias | **17 Plan y casos de prueba** | Cada RF-R0x ya tiene una prueba unitaria; E6 escribe los casos de prueba de sistema (p. ej. CP-R01 "ranking general con datos de ejemplo") |
| Salida esperada del README | **18 Registro de defectos** | Si el resultado obtenido difiere del esperado, se registra un defecto contra RF-R01 |
| Script SQL + diagrama de componentes | **19 Plan de despliegue** | Requisitos de instalación: Python 3.10+, MariaDB 10.6+, ejecutar `02_modelo_datos.sql` |
| Plan de iteración (criterios) | **Plan de iteración C2** | Lo no cumplido (RNF-R01, conexión MariaDB) pasa a C2 |

## 4. Cadena completa de un requisito (ejemplo)
```
RF-R02 Puntaje = 3V + 1E
  → CU-R01 paso 2
  → Estadistica.puntaje (diagrama de clases)
  → estadistica.puntaje  AS (3*victorias + empates)  (modelo de datos)
  → modelo.py: Estadistica.puntaje                    (código)
  → test_rf_r02_formula_de_puntaje                    (prueba unitaria)
  → CP-R02 de E6                                      (caso de prueba)
```
