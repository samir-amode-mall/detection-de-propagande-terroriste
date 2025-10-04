import sys
import os
import bcrypt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_config import get_db_connection


def hash_password(password):
    """Hash du mot de passe avec bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def create_user(username, password, email, role="user"):
    """Ajoute un utilisateur dans la base"""
    conn = get_db_connection()
    if conn is None:
        print("Impossible de se connecter à la base.")
        return

    cursor = conn.cursor()
    password_hash = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, email, role) VALUES (%s, %s, %s, %s)",
            (username, password_hash, email, role)
        )
        conn.commit()
        print(f"Utilisateur {username} créé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'insertion : {e}")

    cursor.close()
    conn.close()

# Exécuter ce script pour ajouter un utilisateur test
if __name__ == "__main__":
    create_user("agent007", "SuperMotDePasseSecurisé!", "agent007@renseignement.com")
    create_user("user1", "mdp1", "mail1")
