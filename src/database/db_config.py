import sqlite3
import os

# Chemin absolu vers le fichier users.db dans src/database/
DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except Exception as e:
        print(f"Erreur de connexion à la base SQLite : {e}")
        return None
