from src.database.db_config import get_db_connection

def create_users_table():
    conn = get_db_connection()
    if conn is None:
        print("Impossible de se connecter à la base de données.")
        return

    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role TEXT DEFAULT 'user',
                two_factor_secret TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("Table users créée (ou déjà existante).")
    except Exception as e:
        print(f"Erreur lors de la création de la table : {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_users_table()
