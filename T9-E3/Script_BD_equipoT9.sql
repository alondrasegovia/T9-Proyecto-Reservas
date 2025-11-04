describe reservas;
ALTER TABLE reservas
ADD COLUMN tipo VARCHAR(20),
ADD COLUMN item_id INT,
ADD COLUMN sub_item_id INT,
ADD COLUMN nombre VARCHAR(100),
ADD COLUMN telefono VARCHAR(50),
ADD COLUMN precio DECIMAL(10,2),
ADD COLUMN fecha_reserva DATETIME DEFAULT CURRENT_TIMESTAMP;

CREATE TABLE reservas_backup AS SELECT * FROM reservas;
SHOW COLUMNS FROM reservas;
SELECT * FROM reservas LIMIT 10;
ALTER TABLE reservas DROP COLUMN fecha;

SELECT * FROM reservas ORDER BY fecha_reserva DESC LIMIT 20;

CREATE TABLE IF NOT EXISTS hoteles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    precio INT,
    foto VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS tours (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    precio INT,
    foto VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100),
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP
    -- Puedes agregar más columnas si lo necesitas
);

CREATE TABLE IF NOT EXISTS miembros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    numero VARCHAR(20),
    password VARCHAR(100)
);

INSERT INTO hoteles (nombre, precio, foto) VALUES
('Hotel Altitur', 150000, 'hotel_altitur.jpg'),
('Hotel Pucara', 11000, 'hotel_pucara.jpg'),
('Hotel Pedro de Valdivia', 95000,'hotel_valdivia');


INSERT INTO tours (nombre, precio, foto) VALUES
('Tour Valle de la Luna', 30000, 'tour_valle_luna.jpg'),
('Geysers del Tatio', 40000, 'geysers_tatio.jpg');

-- Tabla de habitaciones para hoteles
CREATE TABLE IF NOT EXISTS habitaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT,
    tipo VARCHAR(50),
    precio INT,
    foto VARCHAR(100),
    FOREIGN KEY (hotel_id) REFERENCES hoteles(id)
);

-- Tabla de opciones para tours
CREATE TABLE IF NOT EXISTS opciones_tour (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tour_id INT,
    nombre VARCHAR(100),
    precio INT,
    descripcion VARCHAR(255),
    FOREIGN KEY (tour_id) REFERENCES tours(id)
);

INSERT INTO habitaciones (hotel_id, tipo, precio, foto) VALUES
(7, 'Single', 210000, 'habitacion_single1.jpeg'),
(7, 'Doble', 250000, 'habitacion_doble1.jpeg'),
(7, 'Suite', 310000, 'habitacion_suite1.jpeg'),
(8, 'Single', 110000, 'habitacion_single2.jpeg'),
(8, 'Doble', 150000, 'habitacion_doble2.jpeg'),
(8, 'Suite', 200000, 'habitacion_suite2.jpeg'),
(9,	'Single', 95000, 'habitacion_single3.jpeg'),
(9,	'Doble', 110000, 'habitacion_doble3.jpeg'),
(9,	'Suite', 140000, 'habitacion_suite3.jpeg');
				
INSERT INTO tours (nombre, precio, foto) VALUES
('Tour Valle De La Luna', 45000, )

INSERT INTO opciones_tour (tour_id, nombre, precio, descripcion) VALUES
(1, 'Tour premiun', 45000, 'Recorrido por el Valle de la Luna'),
(2, 'Tour básico', 55000, 'Tour Bellazas Deserticas');