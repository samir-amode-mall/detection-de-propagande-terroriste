import sqlite3
import bcrypt
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

def create_user(username, password, email, role="user"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Hachage du mot de passe
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

    try:
        cursor.execute("""
            INSERT OR REPLACE INTO users (username, password_hash, email, role)
            VALUES (?, ?, ?, ?)
        """, (username, password_hash, email, role))
        conn.commit()
        print(f" Utilisateur '{username}' ajouté avec succès.")
    except Exception as e:
        print(f" Erreur pour l'utilisateur '{username}' : {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print(" Initialisation des utilisateurs dans users.db...")

    create_user("admin", "adminpass", "admin@example.com", role="admin")
    create_user("demo", "demo123", "demo@example.com")

    print("Initialisation terminée.")
