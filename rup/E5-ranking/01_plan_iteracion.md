# 14 · Plan de iteración — Construcción C1

**Módulo:** Ranking y estadísticas · **Equipo:** E5 · **Rol RUP:** Jefe de proyecto + Implementador
**Dueño del artefacto:** David Rivera
**Fase:** Construcción · **Iteración:** C1 (primera de 2 en Construcción)
**Duración:** 2 semanas — 17/11/2026 a 30/11/2026
**Viene de:** Plan de desarrollo (E1) → **alimenta a:** Código fuente, evaluación de iteración, plan de C2

## 1. Objetivo de la iteración (una frase)
Entregar un componente ejecutable que calcule y muestre el ranking de personajes ordenado por puntaje, con filtro por clase, sobre un modelo de datos MariaDB que ya incluya la tabla `estadistica`.

## 2. Casos de uso y requisitos incluidos

| ID | Descripción | Entra en C1 |
|----|-------------|:-----------:|
| CU-R01 | Consultar ranking | ✔ completo |
| CU-R02 | Consultar estadísticas de personaje | ✔ flujo básico + A2 |
| RF-R01 | Mostrar ranking ordenado por puntaje descendente (solo personajes con ≥ 1 combate) | ✔ |
| RF-R02 | Puntaje = 3 × victorias + 1 × empates | ✔ |
| RF-R03 | Filtrar ranking por clase (Guerrero, Mago, Arquero) | ✔ |
| RF-R04 | Mostrar combates, victorias, derrotas, empates y % de victorias de un personaje | ✔ |
| RF-R05 | Limitar el ranking a un top N (10 por defecto) | ✔ |
| RNF-R01 | Ranking de 10.000 personajes en < 2 s | ✘ pasa a C2 (prueba de carga) |
| — | Conexión real a MariaDB desde Python | ✘ pasa a C2 (en C1 se usa repositorio en memoria) |

## 3. Tareas, responsables y estimación

| # | Tarea | Responsable | Estim. (h) | Artefacto que produce |
|---|-------|-------------|:---:|---|
| T1 | Ajustar este plan, seguimiento diario y cierre | David Rivera | 4 | 14 Plan de iteración |
| T2 | Diagrama ER (PK, FK, tipos, cardinalidades) | Cesar Riascos | 5 | 15 Modelo de datos (.puml/.png) |
| T3 | Script SQL MariaDB + vista `vista_ranking` + datos de ejemplo | Cesar Riascos | 4 | 15 Modelo de datos (.sql) |
| T4 | Entidades `Personaje`, `Estadistica`, `EntradaRanking` | Juan Delgado | 3 | 16 Código (`modelo.py`) |
| T5 | `RankingService.calcular_ranking()` y `consultar_estadisticas()` | Juan Delgado | 6 | 16 Código (`servicio.py`) |
| T6 | Pruebas unitarias trazadas a RF (13 casos) | Juan Delgado | 4 | 16 Código (`tests/`) |
| T7 | `EstadisticaRepository` (memoria + esqueleto MariaDB) | Juan Delgado | 5 | 16 Código (`repositorio.py`) |
| T8 | Integración: `main.py`, diagrama de componentes, README del componente | David Rivera | 4 | 16 Componentes |
| T9 | Eslabón de trazabilidad y revisión de coherencia de nombres | David Alejandro Villamil | 4 | 00 Eslabón |
| T10 | Preguntas de la dinámica y presentación (máx. 8 diapositivas) | David Alejandro Villamil | 5 | preguntas_dinamica.md, presentacion.pdf |
| T11 | Demo y evaluación de la iteración (los 4 asistentes, 1 h c/u) | Todos | 4 | Evaluación de iteración |
| | **Total** | | **48 h** | |

## 4. Criterio de evaluación al cerrar la iteración
La iteración C1 se da por **exitosa** si se cumplen todos:
1. Las 13 pruebas unitarias pasan (`python -m unittest discover -s tests` → `OK`).
2. Con los datos de ejemplo, el ranking general muestra el orden Eldrin (27) → Sylva (25) → Torvak (25) → Brena (25) → Merlina (11) → Robin (3), y *Novato* (0 combates) no aparece.
3. El script `02_modelo_datos.sql` se ejecuta sin errores en MariaDB 10.6 y `SELECT * FROM vista_ranking` devuelve el mismo orden del punto 2.
4. Cada RF-R01…R05 aparece en el README del código con el archivo/método que lo implementa.
5. Revisión de coherencia: los nombres `personaje`, `estadistica`, `RankingService`, `calcular_ranking` son idénticos en ER, SQL, código y diagrama de componentes.

Lo que no se cumpla pasa como tarea al **plan de la iteración C2**, junto con los defectos que reporte E6 en su registro.

## 5. Comparación con un Sprint de Scrum

| Aspecto | Iteración RUP (C1) | Sprint de Scrum |
|---|---|---|
| Duración | Fija (2 semanas aquí) | Fija (time-box de 1–4 semanas) |
| Resultado | Incremento ejecutable | Incremento potencialmente entregable |
| Qué se planea | **Casos de uso y requisitos** priorizados por riesgo | **Historias de usuario** del Product Backlog |
| Quién planea | Jefe de proyecto asigna tareas a roles | El equipo se auto-organiza; nadie asigna |
| Marco mayor | Pertenece a una **fase** (Construcción) con un hito | No hay fases: todos los sprints son iguales |
| Documentación | Produce/actualiza artefactos formales (ER, SAD, plan) | Mínima; prioriza software funcionando |
| Cierre | Evaluación de iteración contra criterios del plan | Sprint Review + Retrospectiva |

**En qué se parecen:** ambos son iterativos e incrementales, tienen duración fija, terminan con algo que funciona y usan lo aprendido para planear el siguiente ciclo.
**En qué no:** en RUP la iteración está dirigida por casos de uso y encajada en fases con hitos, y los roles están definidos; en Scrum no hay fases, el equipo se auto-organiza y el compromiso es con un Sprint Goal.
