import sqlite3
import hashlib
from datetime import datetime

def init_database():
    """Initialiser la base de données StudyBuddy+"""
    conn = sqlite3.connect('studybuddy.db')
    cursor = conn.cursor()
    
    # Table utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pseudo VARCHAR(100) UNIQUE NOT NULL,
            mot_de_passe_hash VARCHAR(255) NOT NULL,
            date_inscription DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table méthodes de travail
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS methodes_travail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom VARCHAR(50) NOT NULL,
            duree_session INTEGER NOT NULL,
            duree_pause INTEGER NOT NULL,
            description TEXT
        )
    ''')
    
    # Table sessions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            utilisateur_id INTEGER NOT NULL,
            methode_id INTEGER NOT NULL,
            date_debut DATETIME,
            date_fin DATETIME,
            duree_reelle INTEGER,
            statut TEXT DEFAULT 'en_cours',
            FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id),
            FOREIGN KEY (methode_id) REFERENCES methodes_travail(id)
        )
    ''')
    
    # Insérer les méthodes de travail
    cursor.execute('''SELECT COUNT(*) FROM methodes_travail''')
    if cursor.fetchone()[0] == 0:
        methodes = [
            ('Pomodoro Classique', 25, 5, '25min travail / 5min pause'),
            ('Pomodoro Long', 50, 10, '50min travail / 10min pause'),
            ('Focus Intense', 90, 15, '90min travail / 15min pause'),
            ('Session Rapide', 15, 3, '15min travail / 3min pause')
        ]
        cursor.executemany('''INSERT INTO methodes_travail (nom, duree_session, duree_pause, description) 
                              VALUES (?, ?, ?, ?)''', methodes)
    
    conn.commit()
    conn.close()
    print("✅ Base de données initialisée!")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

if __name__ == "__main__":
    init_database()
