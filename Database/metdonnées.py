#!/usr/bin/python3

import json
from mysql import connector
from utils import conn_to_ddb

# Charger le fichier JSON
with open('data.json', 'r') as file:
    data = json.load(file)

# Connexion à la base de données MySQL
conn = conn_to_ddb()
cursor = conn.cursor()

# Préparer la requête d'insertion
insert_query = """
INSERT INTO Books (ISBN, title, author, editor, release_date, couverture, summary)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# Insérer les données
for entry in data:
    try:
        cursor.execute(insert_query,
                       (entry['ISBN'], entry['Titre'], entry['Auteur'],
                        entry['Editeur'], entry['Date de sortie'],
                        entry['Couverture'], entry['Résumé']))
    except connector.IntegrityError as e:
        print(f"Ignorer l'insertion pour ISBN {entry['ISBN']}. Doublon détecté.")

# Valider les modifications
conn.commit()

# Fermer la connexion
cursor.close()
conn.close()
