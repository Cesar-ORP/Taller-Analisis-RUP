-- =====================================================================
-- RPG Manager · Módulo Ranking y estadísticas (Equipo E5)
-- Artefacto 15: Modelo de datos · Motor: MariaDB 10.6+ (InnoDB, utf8mb4)
-- Dueño: Cesar Riascos · Iteración C1
-- =====================================================================
CREATE DATABASE IF NOT EXISTS rpg_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE rpg_manager;

-- Jugador: dueño de la cuenta (lo gestiona E6, aquí versión mínima)
CREATE TABLE jugador (
    id_jugador      INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    nombre_usuario  VARCHAR(30)   NOT NULL,
    correo          VARCHAR(100)  NOT NULL,
    fecha_registro  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_jugador PRIMARY KEY (id_jugador),
    CONSTRAINT uq_jugador_usuario UNIQUE (nombre_usuario),
    CONSTRAINT uq_jugador_correo  UNIQUE (correo)
) ENGINE = InnoDB;

-- Personaje: 1 jugador tiene 0..N personajes
CREATE TABLE personaje (
    id_personaje  INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    id_jugador    INT UNSIGNED      NOT NULL,
    nombre        VARCHAR(30)       NOT NULL,
    clase         ENUM('Guerrero','Mago','Arquero') NOT NULL,
    nivel         TINYINT UNSIGNED  NOT NULL DEFAULT 1,
    experiencia   INT UNSIGNED      NOT NULL DEFAULT 0,
    CONSTRAINT pk_personaje PRIMARY KEY (id_personaje),
    CONSTRAINT uq_personaje_nombre UNIQUE (nombre),
    CONSTRAINT fk_personaje_jugador FOREIGN KEY (id_jugador)
        REFERENCES jugador (id_jugador) ON DELETE CASCADE,
    CONSTRAINT ck_personaje_nivel CHECK (nivel BETWEEN 1 AND 100)
) ENGINE = InnoDB;

-- Combate: enfrenta a 2 personajes; id_ganador NULL = empate
CREATE TABLE combate (
    id_combate     INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    id_personaje_1 INT UNSIGNED      NOT NULL,
    id_personaje_2 INT UNSIGNED      NOT NULL,
    id_ganador     INT UNSIGNED      NULL,
    turnos         SMALLINT UNSIGNED NOT NULL,
    fecha          DATETIME          NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_combate PRIMARY KEY (id_combate),
    CONSTRAINT fk_combate_p1 FOREIGN KEY (id_personaje_1) REFERENCES personaje (id_personaje),
    CONSTRAINT fk_combate_p2 FOREIGN KEY (id_personaje_2) REFERENCES personaje (id_personaje),
    CONSTRAINT fk_combate_ganador FOREIGN KEY (id_ganador) REFERENCES personaje (id_personaje),
    CONSTRAINT ck_combate_distintos CHECK (id_personaje_1 <> id_personaje_2),
    CONSTRAINT ck_combate_ganador CHECK (id_ganador IS NULL
        OR id_ganador = id_personaje_1 OR id_ganador = id_personaje_2)
) ENGINE = InnoDB;

-- Estadistica: 1 personaje tiene exactamente 1 estadística (1:1 por UNIQUE en la FK)
CREATE TABLE estadistica (
    id_estadistica      INT UNSIGNED NOT NULL AUTO_INCREMENT,
    id_personaje        INT UNSIGNED NOT NULL,
    victorias           INT UNSIGNED NOT NULL DEFAULT 0,
    derrotas            INT UNSIGNED NOT NULL DEFAULT 0,
    empates             INT UNSIGNED NOT NULL DEFAULT 0,
    combates_jugados    INT UNSIGNED AS (victorias + derrotas + empates) PERSISTENT,
    puntaje             INT UNSIGNED AS (3 * victorias + empates) PERSISTENT,   -- RF-R02
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT pk_estadistica PRIMARY KEY (id_estadistica),
    CONSTRAINT uq_estadistica_personaje UNIQUE (id_personaje),
    CONSTRAINT fk_estadistica_personaje FOREIGN KEY (id_personaje)
        REFERENCES personaje (id_personaje) ON DELETE CASCADE
) ENGINE = InnoDB;

-- Índice para RNF-R01 (ranking de 10.000 personajes en < 2 s)
CREATE INDEX ix_estadistica_ranking ON estadistica (puntaje DESC, victorias DESC, derrotas ASC);

-- Vista que usa EstadisticaRepositoryMariaDB (RF-R01, RF-R03)
CREATE VIEW vista_ranking AS
SELECT p.id_personaje, p.nombre, p.clase, e.victorias, e.derrotas, e.empates,
       e.combates_jugados, e.puntaje
FROM personaje p
JOIN estadistica e ON e.id_personaje = p.id_personaje
WHERE e.combates_jugados > 0
ORDER BY e.puntaje DESC, e.victorias DESC, e.derrotas ASC, p.nombre ASC;

-- Datos de ejemplo (los mismos de main.py)
INSERT INTO jugador (nombre_usuario, correo) VALUES
 ('drivera','drivera@rpg.test'), ('criascos','criascos@rpg.test'),
 ('dvillamil','dvillamil@rpg.test'), ('jdelgado','jdelgado@rpg.test');
INSERT INTO personaje (id_jugador, nombre, clase, nivel) VALUES
 (1,'Torvak','Guerrero',12), (1,'Eldrin','Mago',15), (2,'Sylva','Arquero',11),
 (2,'Merlina','Mago',7), (3,'Brena','Guerrero',9), (3,'Robin','Arquero',4), (4,'Novato','Mago',1);
INSERT INTO estadistica (id_personaje, victorias, derrotas, empates) VALUES
 (1,8,2,1), (2,9,1,0), (3,8,1,1), (4,3,5,2), (5,8,3,1), (6,1,4,0), (7,0,0,0);

-- Consulta del ranking (top 10 de Magos)
-- SELECT * FROM vista_ranking WHERE clase = 'Mago' LIMIT 10;
