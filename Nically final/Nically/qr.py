from cs50 import SQL

# Conectar a la base de datos
db = SQL("sqlite:///users.db")

# Limpiar tablas existentes
tables = ["user_responses", "user_trivias", "responses", "questions", "trivias", "categories", "achievements", "user_achievements"]
for table in tables:
    db.execute(f"DELETE FROM {table};")

# Insertar logros
db.execute("""
    INSERT INTO achievements (achievement_id, title, description) VALUES
    (1, 'Principiante', 'Completaste 1 trivia.'),
    (2, 'Uwu', 'Completaste 3 trivias.'),
    (3, 'Pinolero', 'Completaste todas las trivias.');
""")

# Insertar categorías
db.execute("""
    INSERT INTO categories (category_id, name) VALUES
    (1, 'Cultura General'),
    (2, 'Historia'),
    (3, 'Gastronomía'),
    (4, 'Arte'),
    (5, 'Tradiciones');
""")

# Insertar trivias
db.execute("""
    INSERT INTO trivias (trivia_id, user_id, category_id, title, image, points) VALUES
    (1, NULL, 1, 'Símbolos Nacionales de Nicaragua', '/static/Simbolos_nacionales.jpg', 10),
    (2, NULL, 2, 'Historia de Nicaragua', '/static/historia.jpg', 15),
    (3, NULL, 3, 'Gastronomía Nicaragüense', '/static/gastronomia.jpg', 20),
    (4, NULL, 4, 'Literatura Nicaragüense', '/static/literatura.jpg', 25),
    (5, NULL, 5, 'Leyendas de Nicaragua', '/static/leyendas.jpg', 30),
    (6, NULL, 1, 'Festividades', '/static/cultura_general.jpg', 10),
    (7, NULL, 3, 'Comidas', '/static/animales.jpg', 15),
    (8, NULL, 2, 'Clima de Nicaragua', '/static/clima.jpg', 20),
    (9, NULL, 5, 'Idiomas Indígenas', '/static/idiomas.jpg', 25),
    (10, NULL, 4, 'El Güegüense', '/static/gueguense.jpg', 30);
""")



# Insertar preguntas y respuestas para Trivia 1: Símbolos Nacionales de Nicaragua
db.execute("""
    INSERT INTO questions (question_id, trivia_id, question_text) VALUES
    (1, 1, '¿Cuál es el símbolo nacional de Nicaragua que aparece en el centro de la bandera?'),
    (2, 1, '¿Qué representan los cinco volcanes en el escudo de armas de Nicaragua?'),
    (3, 1, '¿Cuál es la flor nacional de Nicaragua?');
""")

db.execute("""
    INSERT INTO responses (response_id, question_id, trivia_id, response_text, correct) VALUES
    (1, 1, 1, 'Un triángulo equilátero', 1),
    (2, 1, 1, 'Un rectángulo azul', 0),
    (3, 1, 1, 'Un círculo dorado', 0),
    (4, 2, 1, 'Los cinco países de Centroamérica', 1),
    (5, 2, 1, 'Las cinco montañas más altas', 0),
    (6, 2, 1, 'Las cinco luchas por la independencia', 0),
    (7, 3, 1, 'Sacuanjoche', 1),
    (8, 3, 1, 'Flor de Mayo', 0),
    (9, 3, 1, 'Jazmín', 0);
""")

# Insertar preguntas y respuestas para Trivia 2: Historia de Nicaragua
db.execute("""
    INSERT INTO questions (question_id, trivia_id, question_text) VALUES
    (4, 2, '¿En qué año se independizó Nicaragua de España?'),
    (5, 2, '¿Qué conflicto armado ocurrió en Nicaragua entre 1981 y 1990?'),
    (6, 2, '¿Quién fue el líder del Frente Sandinista de Liberación Nacional (FSLN) que llegó al poder en 1979?');
""")

db.execute("""
    INSERT INTO responses (response_id, question_id, trivia_id, response_text, correct) VALUES
    (10, 4, 2, '1821', 1),
    (11, 4, 2, '1905', 0),
    (12, 4, 2, '1838', 0),
    (13, 5, 2, 'La Guerra de los Contras', 1),
    (14, 5, 2, 'La Revolución Liberal', 0),
    (15, 5, 2, 'La Guerra Fría', 0),
    (16, 6, 2, 'Daniel Ortega', 1),
    (17, 6, 2, 'Anastasio Somoza', 0),
    (18, 6, 2, 'Violeta Barrios', 0);
""")

# Insertar preguntas y respuestas para Trivia 3: Gastronomía Nicaragüense
db.execute("""
    INSERT INTO questions (question_id, trivia_id, question_text) VALUES
    (7, 3, '¿Cuál es el plato nacional de Nicaragua?'),
    (8, 3, '¿Qué bebida tradicional se elabora con maíz fermentado?'),
    (9, 3, '¿Qué dulce típico es originario de León?');
""")

db.execute("""
    INSERT INTO responses (response_id, question_id, trivia_id, response_text, correct) VALUES
    (19, 7, 3, 'Gallo Pinto', 1),
    (20, 7, 3, 'Baho', 0),
    (21, 7, 3, 'Vigorón', 0),
    (22, 8, 3, 'Chicha', 1),
    (23, 8, 3, 'Pinolillo', 0),
    (24, 8, 3, 'Cacao', 0),
    (25, 9, 3, 'Cajeta de leche', 1),
    (26, 9, 3, 'Rosquillas', 0),
    (27, 9, 3, 'Turrón', 0);
""")

# Insertar preguntas y respuestas para Trivia 4: Literatura Nicaragüense
db.execute("""
    INSERT INTO questions (question_id, trivia_id, question_text) VALUES
    (10, 4, '¿Quién es considerado el poeta más importante de Nicaragua?'),
    (11, 4, '¿En qué año Rubén Darío publicó *Azul*?'),
    (12, 4, '¿Qué corriente literaria es asociada con Rubén Darío?');
""")

db.execute("""
    INSERT INTO responses (response_id, question_id, trivia_id, response_text, correct) VALUES
    (28, 10, 4, 'Rubén Darío', 1),
    (29, 10, 4, 'Ernesto Cardenal', 0),
    (30, 10, 4, 'Salomón de la Selva', 0),
    (31, 11, 4, '1888', 1),
    (32, 11, 4, '1890', 0),
    (33, 11, 4, '1875', 0),
    (34, 12, 4, 'Modernismo', 1),
    (35, 12, 4, 'Romanticismo', 0),
    (36, 12, 4, 'Realismo', 0);
""")

# Insertar preguntas y respuestas para Trivia 5: Leyendas de Nicaragua
db.execute("""
    INSERT INTO questions (question_id, trivia_id, question_text) VALUES
    (13, 5, '¿Cuál es la leyenda que habla de un espíritu femenino en busca de sus hijos?'),
    (14, 5, '¿Qué leyenda narra sobre una carreta espectral que aparece de noche?'),
    (15, 5, '¿Qué figura mítica protege a los borrachos de la región?');
""")

db.execute("""
    INSERT INTO responses (response_id, question_id, trivia_id, response_text, correct) VALUES
    (37, 13, 5, 'La Llorona', 1),
    (38, 13, 5, 'La Cegua', 0),
    (39, 13, 5, 'La Carreta Nagua', 0),
    (40, 14, 5, 'La Carreta Nagua', 1),
    (41, 14, 5, 'El Cadejo', 0),
    (42, 14, 5, 'La Mocuana', 0),
    (43, 15, 5, 'El Cadejo', 1),
    (44, 15, 5, 'La Cegua', 0),
    (45, 15, 5, 'La Llorona', 0);
""")

# Trivia 6: Fiestas Tradicionales de Nicaragua (Categoría 1)
db.execute("""
    INSERT INTO questions (question_id, trivia_id, question_text) VALUES
    (16, 6, '¿En qué mes se celebra la Purísima en Nicaragua?'),
    (17, 6, '¿Qué ciudad celebra la Fiesta de San Sebastián?'),
    (18, 6, '¿Cuál es la festividad más conocida de Granada?'),
    (19, 6, '¿Qué se lanza durante la Gritería?'),
    (20, 6, '¿Qué santo se celebra en Diriamba en enero?'),
    (21, 6, '¿Qué evento ocurre en honor a Santo Domingo?'),
    (22, 6, '¿Qué festividad incluye el baile de Las Inditas?');
""")

db.execute("""
    INSERT INTO responses (response_id, question_id, trivia_id, response_text, correct) VALUES
    (46, 16, 6, 'Diciembre.', 1),
    (47, 16, 6, 'Julio.', 0),
    (48, 17, 6, 'Diriamba.', 1),
    (49, 17, 6, 'Managua.', 0),
    (50, 18, 6, 'La Gritería.', 1),
    (51, 18, 6, 'El Tope de Toros.', 0),
    (52, 19, 6, 'Caramelos.', 1),
    (53, 19, 6, 'Flores.', 0),
    (54, 20, 6, 'San Sebastián.', 1),
    (55, 20, 6, 'Santo Domingo.', 0),
    (56, 21, 6, 'Procesiones y bailes tradicionales.', 1),
    (57, 21, 6, 'Carreras de caballos.', 0),
    (58, 22, 6, 'Las festividades patronales.', 1),
    (59, 22, 6, 'El carnaval.', 0);
""")

# Trivia 7: Costumbres Nicaragüenses (Categoría 2)
db.execute("""
    INSERT INTO questions (question_id, trivia_id, question_text) VALUES
    (23, 7, '¿Qué costumbre se realiza el 31 de diciembre?'),
    (24, 7, '¿Qué bebida tradicional acompaña las fiestas?'),
    (25, 7, '¿Qué comida típica se prepara en Semana Santa?'),
    (26, 7, '¿Qué es la Chicha Bruja?'),
    (27, 7, '¿Qué se come durante la Purísima?'),
    (28, 7, '¿Qué festividad incluye el uso de máscaras?'),
    (29, 7, '¿Qué costumbre incluye la quema del Viejo?');
""")

db.execute("""
    INSERT INTO responses (response_id, question_id, trivia_id, response_text, correct) VALUES
    (60, 23, 7, 'La quema del Viejo.', 1),
    (61, 23, 7, 'La Gritería.', 0),
    (62, 24, 7, 'Pinolillo.', 1),
    (63, 24, 7, 'Café.', 0),
    (64, 25, 7, 'Sopa de queso.', 1),
    (65, 25, 7, 'Tamal.', 0),
    (66, 26, 7, 'Una bebida fermentada.', 1),
    (67, 26, 7, 'Un dulce típico.', 0),
    (68, 27, 7, 'Ayote en miel.', 1),
    (69, 27, 7, 'Gallo pinto.', 0),
    (70, 28, 7, 'Las fiestas patronales.', 1),
    (71, 28, 7, 'Semana Santa.', 0),
    (72, 29, 7, 'Año Nuevo.', 1),
    (73, 29, 7, 'Fiestas de San Juan.', 0);
""")

# Trivia 8: Clima de Nicaragua (Categoría 3)
db.execute("""
    INSERT INTO questions (question_id, trivia_id, question_text) VALUES
    (30, 8, '¿Cuál es la temporada de lluvias en Nicaragua?'),
    (31, 8, '¿Qué región de Nicaragua es conocida por ser más seca?'),
    (32, 8, '¿Qué fenómeno climático afecta a Nicaragua en la temporada de huracanes?'),
    (33, 8, '¿Cuál es la temperatura promedio en la región del Pacífico?'),
    (34, 8, '¿Qué región tiene el clima más fresco?'),
    (35, 8, '¿En qué época del año hay menos lluvias?'),
    (36, 8, '¿Qué fenómeno ocurre frecuentemente en el Caribe durante octubre?');
""")

db.execute("""
    INSERT INTO responses (response_id, question_id, trivia_id, response_text, correct) VALUES
    (74, 30, 8, 'De mayo a noviembre.', 1),
    (75, 30, 8, 'De diciembre a abril.', 0),
    (76, 31, 8, 'La región del Pacífico.', 1),
    (77, 31, 8, 'La región del Caribe.', 0),
    (78, 32, 8, 'Huracanes y tormentas tropicales.', 1),
    (79, 32, 8, 'Tornados.', 0),
    (80, 33, 8, '25-30°C.', 1),
    (81, 33, 8, '15-20°C.', 0),
    (82, 34, 8, 'La región del Norte.', 1),
    (83, 34, 8, 'La región Central.', 0),
    (84, 35, 8, 'En la época seca.', 1),
    (85, 35, 8, 'En la época húmeda.', 0),
    (86, 36, 8, 'Huracanes.', 1),
    (87, 36, 8, 'Tifones.', 0);
""")

# Trivia 9: Idiomas Indígenas (Categoría 4)
db.execute("""
    INSERT INTO questions (question_id, trivia_id, question_text) VALUES
    (38, 9, '¿Cuál es uno de los idiomas indígenas de Nicaragua?'),
    (39, 9, '¿Qué comunidad habla el idioma miskito?'),
    (40, 9, '¿Qué idioma indígena tiene más hablantes en Nicaragua?'),
    (41, 9, '¿En qué región se encuentran los hablantes de mayangna?'),
    (42, 9, '¿Qué idioma indígena está en peligro de extinción?'),
    (43, 9, '¿Qué idioma es común en la Costa Caribe además del español?'),
    (44, 9, '¿Qué idioma indígena se preserva en las tradiciones locales?');
""")

db.execute("""
    INSERT INTO responses (response_id, question_id, trivia_id, response_text, correct) VALUES
    (88, 38, 9, 'Miskito.', 1),
    (89, 38, 9, 'Quechua.', 0),
    (90, 39, 9, 'Comunidades del Caribe Norte.', 1),
    (91, 39, 9, 'Comunidades del Pacífico.', 0),
    (92, 40, 9, 'Miskito.', 1),
    (93, 40, 9, 'Mayangna.', 0),
    (94, 41, 9, 'En la Costa Caribe.', 1),
    (95, 41, 9, 'En la región del Pacífico.', 0),
    (96, 42, 9, 'Mayangna.', 1),
    (97, 42, 9, 'Miskito.', 0),
    (98, 43, 9, 'Criollo.', 1),
    (99, 43, 9, 'Francés.', 0),
    (100, 44, 9, 'Miskito.', 1),
    (101, 44, 9, 'Nahuatl.', 0);
""")

# Trivia 10: El Güegüense (Categoría 5)
db.execute("""
    INSERT INTO questions (question_id, trivia_id, question_text) VALUES
    (45, 10, '¿Qué es El Güegüense?'),
    (46, 10, '¿En qué ciudad se representa El Güegüense?'),
    (47, 10, '¿Qué personaje es el protagonista en El Güegüense?'),
    (48, 10, '¿Qué género teatral pertenece El Güegüense?'),
    (49, 10, '¿Qué representa El Güegüense en la cultura nicaragüense?'),
    (50, 10, '¿En qué siglo se originó El Güegüense?'),
    (51, 10, '¿Qué idioma mezcla El Güegüense en sus diálogos?');
""")

db.execute("""
    INSERT INTO responses (response_id, question_id, trivia_id, response_text, correct) VALUES
    (102, 45, 10, 'Una obra teatral y danza.', 1),
    (103, 45, 10, 'Un poema.', 0),
    (104, 46, 10, 'Diriamba.', 1),
    (105, 46, 10, 'León.', 0),
    (106, 47, 10, 'El Güegüense.', 1),
    (107, 47, 10, 'El Alcalde Real.', 0),
    (108, 48, 10, 'Comedia satírica.', 1),
    (109, 48, 10, 'Drama trágico.', 0),
    (110, 49, 10, 'La resistencia indígena.', 1),
    (111, 49, 10, 'La colonización española.', 0),
    (112, 50, 10, 'Siglo XVII.', 1),
    (113, 50, 10, 'Siglo XIX.', 0),
    (114, 51, 10, 'Español y náhuatl.', 1),
    (115, 51, 10, 'Español e inglés.', 0);
""")


print("Datos insertados correctamente.")

