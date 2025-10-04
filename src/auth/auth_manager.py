import bcrypt
import jwt
import datetime
import sys
import os
import importlib.util

# Ajouter `src/` au chemin de recherche Python pour que `database` soit trouvé
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'db_config.py'))
module_name = "database.db_config"

spec = importlib.util.spec_from_file_location(module_name, module_path)
db_config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(db_config)

get_db_connection = db_config.get_db_connection

SECRET_KEY = "super-secret-key"

def verify_password(password, hashed_password):
    """Vérifie si un mot de passe correspond au hash"""
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def generate_token(username):
    """Génère un token JWT valable 30 minutes"""
    payload = {
        "sub": username,
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def login(username, password):
    """Vérifie les identifiants et retourne un JWT"""
    conn = get_db_connection()
    if conn is None:
        return {"message": "Erreur de connexion à la base"}, 500

    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username=?", (username,))

    user = cursor.fetchone()
    conn.close()

    if not user or not verify_password(password, user[0]):
        return {"message": "Identifiants incorrects"}, 401

    token = generate_token(username)
    return {"access_token": token}, 200

# Tester l'authentification depuis le terminal
if __name__ == "__main__":
    username = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")
    
    response, status = login(username, password)
    
    if status == 200:
        print(f"Connexion réussie ! Token : {response['access_token']}")
    else:
        print(f" Erreur : {response['message']}")
