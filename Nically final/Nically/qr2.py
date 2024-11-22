from cs50 import SQL

# Conectar a la base de datos
db = SQL("sqlite:///users.db")

db.execute("ALTER TABLE user_responses ADD COLUMN attempted BOOLEAN DEFAULT 0;")
