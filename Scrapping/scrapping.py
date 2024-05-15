#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import json


def get_all_pages():
    """"""
    urls = []
    page_number = 202
    for i in range(407):
        i = f'https://www.placedeslibraires.fr/listeliv.php?rayon=Policier+%26+Thriller%7CThriller&select_tri_recherche=dateparution_decroissant&base=allbooks&codegtl1=90000000&codegtl2=90020000&page={page_number}'
        page_number += 1
        urls.append(i)

    return urls


def parse_books(url):
    """"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    livres = soup.find_all('div', class_='meta_produit col-md-10 col-xs-8 no-padding')
    couverture = soup.find_all('div', class_='col-xs-4 text-center mb-01 col-md-2')

    json_data = []
    for livre, img in zip(livres, couverture):
        ISBN_element = livre.find('li', string=lambda texte: texte and texte.strip().isdigit())
        if ISBN_element:
            ISBN_livre = ISBN_element.text.strip()
        titre_livre = livre.find('h2', class_='livre_titre').a.text.strip()
        try:
            auteur_livre = livre.find('h2', class_='livre_auteur').a.text.strip()
        except AttributeError as e:
            auteur_livre = ""
        try:
            editeur_livre = livre.find('li', class_='editeur').span.text.strip()
        except AttributeError as e:
            editeur_livre = ""
        try:
            sortie_livre = livre.find('li', class_='MiseEnLigne').text.strip()
        except AttributeError as e:
            sortie_livre = ""
        img_livre = img.find('img', class_='lazy')
        try:
            couverture_livre = img_livre['data-src']
        except TypeError as e:
            couverture_livre = ""

        dict_livres = {
            'Titre': titre_livre,
            'Auteur': auteur_livre,
            'Editeur': editeur_livre,
            'Date de sortie': sortie_livre,
            'ISBN': ISBN_livre,
            'Couverture': couverture_livre
        }
        json_data.append(dict_livres)

    try:
        with open('books_file.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        data = []

    data_to_file = data + json_data

    with open('books_file_thriller.json', 'w', encoding='utf-8') as f:
        json.dump(data_to_file, f, ensure_ascii=False, indent=4)


def parse_all_pages():
    """"""
    pages = get_all_pages()
    for page in pages[:206]:
        parse_books(url=page)
        print(f'{page}')


parse_all_pages()
