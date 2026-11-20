# Dinámica de preguntas — E5 Construcción (Ranking y estadísticas)

**Formato:** tarjetas A/B/C por filas (cada fila responde en grupo, 1 min por pregunta).
**Responsable:** David Alejandro Villamil

---

## P1 · ¿Qué artefacto usarías?
Termina la iteración C1. El profesor (cliente) pregunta: *"¿El ranking ya debía responder en menos de 2 segundos con 10.000 personajes, o eso quedó para después?"* ¿Dónde buscas la respuesta?

- A) Modelo de datos
- **B) Plan de iteración** ✅
- C) README del código fuente

**Respuesta:** B. El plan de iteración C1 dice qué requisitos entran y cuáles no: RNF-R01 está marcado como "pasa a C2".
**Por qué fallan las otras:** el modelo de datos tiene un índice pensado para ese RNF, pero no dice *cuándo* se cumple; el README dice qué RF implementa el código, no qué se comprometió en cada iteración.

---

## P2 · Encuentra el error (modelo de datos)
Este fragmento del script dice ser la tabla de estadísticas, donde **cada personaje tiene una sola estadística**:

```sql
CREATE TABLE estadistica (
    id_estadistica INT UNSIGNED NOT NULL AUTO_INCREMENT,
    id_personaje   INT UNSIGNED NOT NULL,
    victorias      INT UNSIGNED NOT NULL DEFAULT 0,
    derrotas       INT UNSIGNED NOT NULL DEFAULT 0,
    CONSTRAINT pk_estadistica PRIMARY KEY (id_estadistica),
    CONSTRAINT fk_estadistica_personaje FOREIGN KEY (id_personaje)
        REFERENCES jugador (id_jugador)
);
```
¿Qué está mal?

**Respuesta (hay 2 errores plantados):**
1. La FK apunta a `jugador (id_jugador)` y debe apuntar a `personaje (id_personaje)`. Las estadísticas son del personaje, no de la cuenta del jugador (así está en el modelo del dominio y en el ER).
2. Falta `UNIQUE (id_personaje)`. Sin él la relación queda 1:N y un personaje podría tener dos filas de estadísticas y salir dos veces en el ranking. La cardinalidad del ER es 1:1.

**Bonus:** falta la columna `empates`, y RF-R02 la necesita para calcular el puntaje.

---

## P3 · Encuentra el error (código) y ¿quién lo detecta?
Un compañero cambió esta línea en `servicio.py`:
```python
filas.sort(key=lambda pe: (pe[1].puntaje, -pe[1].victorias, pe[1].derrotas, pe[0].nombre.lower()))
```
¿Qué pasa y qué artefacto lo debería detectar primero?

- A) Nada, el orden es el mismo
- B) El ranking sale al revés (el peor primero); lo detecta el **diagrama de componentes**
- **C) El ranking sale al revés (el peor primero); lo detecta la prueba trazada a RF-R01 y se anota en el Registro de defectos** ✅

**Respuesta:** C. Se perdió el `-` delante de `puntaje` y el orden queda ascendente. La prueba `test_rf_r01_orden_por_puntaje_descendente` falla, y en la fase de E6 se registra como defecto de severidad alta contra RF-R01.
**Por qué fallan las otras:** A no cambia nada, y el error sí cambia el orden. B describe bien el síntoma, pero un diagrama de componentes muestra la estructura, no el comportamiento.

---

## P4 · ¿Qué artefactos cambian? (pensamiento iterativo)
En la iteración C2 el cliente decide que **la victoria vale 2 puntos y no 3**. ¿Cuáles de nuestros artefactos hay que tocar?

**Respuesta:**
- **Requisitos** (RF-R02): se cambia la fórmula y es el origen del cambio.
- **Modelo de datos**: hay que cambiar la columna calculada `puntaje AS (2*victorias + empates)`.
- **Código**: hay que cambiar la constante `PUNTOS_VICTORIA = 2` en `modelo.py`.
- **Pruebas**: `test_rf_r02_formula_de_puntaje` y el orden esperado de `test_rf_r01_*` (y los casos de prueba de E6).
- **Plan de iteración C2**: hay que agregar la tarea con su responsable.

**Idea clave:** en RUP los artefactos **evolucionan**; no se escriben una sola vez. Si solo se cambia el código, el SQL sigue calculando con 3 y la base de datos y la aplicación muestran rankings distintos. Esa es justo la inconsistencia que más cuesta encontrar.

---

## Pregunta de auditoría cruzada para E6 (Cuentas de jugador y sesión)
> Versión preparada; se ajusta tras revisar su carpeta en el repositorio.

"En su caso de prueba de **bloqueo tras 3 intentos**, ¿qué pasa en el 4.º intento *después* de que pase el tiempo de bloqueo? No encontramos el flujo alternativo de **desbloqueo** en la especificación del CU *Iniciar sesión* ni un caso de prueba que lo verifique. ¿Qué RNF define cuánto dura el bloqueo?"
