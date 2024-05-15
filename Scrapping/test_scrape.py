#!/usr/bin/python3

import requests

API_KEY = 'AIzaSyAq0COD7e_Ue2sP_h3eIofkTyj9pcjbrYE'
author_name = 'Guillaume Musso'
url = f'https://www.googleapis.com/books/v1/volumes?q=inauthor:{author_name}&key={API_KEY}'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    if 'items' in data:
        # Parcourir les résultats et afficher toutes les informations relatives aux 50 premiers livres en français
        for item in data['items']:
            volume_info = item.get('volumeInfo', {})
            print("Titre:", volume_info.get('title'))
            print("Auteurs:", volume_info.get('authors', 'Inconnu'))
            print("Date de publication:", volume_info.get('publishedDate'))
            # Extraction des ISBN-13 seulement
            isbn_13_list = [identifier['identifier'] for identifier in volume_info.get('industryIdentifiers', []) if identifier.get('type') == 'ISBN_13']
            print("ISBN-13:", isbn_13_list)
            print("Nombre de pages:", volume_info.get('pageCount'))
            print("Catégorie:", volume_info.get('categories'))
            print()
    else:
        print('Aucun résultat trouvé pour cette recherche.')
else:
    print('Erreur lors de la requête : ', response.status_code)
