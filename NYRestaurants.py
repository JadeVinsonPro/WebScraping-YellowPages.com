import requests
from bs4 import BeautifulSoup
import csv

def scrape_page(soup, restaurants):
    # récupération de toutes les <div> HTML dans la page
    restaurant_elements = soup.find_all('div', class_='info')
    informations_elements = soup.find_all('div', class_='info-section info-secondary')

    # iterating over the list of restaurant elements
    # to extract the data of interest and store it
    # in restaurants
    for restaurant_element in restaurant_elements:

        nom = restaurant_element.find('span').text
        tag_elements = restaurant_element.find('div', class_='categories').find_all('a')
        adresse = restaurant_element.find('div', class_='street-address')
        if adresse is not None:
            a = adresse.text

        ville = restaurant_element.find('div', class_='locality')
        if ville is not None:
            v = ville.text

        tel = restaurant_element.find('div', class_="phones phone primary")
        if tel is not None:
            x = tel.text

        # génération d'une liste de tous les tags par restaurant
        tags = []
        for tag_element in tag_elements:
            tags.append(tag_element.text)

        # génération de dictionnaire qui contient les données des restaurants
        restaurants.append(
            {
                'nom': nom,
                'tags': ', '.join(tags),# Suite des tags séparés par des virgules
                'adresse': a,
                'ville': v,
                'phones phone primary': x

            }
        )

# URL du site à scrapper
base_url = 'https://www.yellowpages.com/new-york-ny/restaurants'

# defining the User-Agent header to use in the GET request below
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

# retrieving the target web page
page = requests.get(base_url, headers=headers)

# pweb parsing avec Beautiful Soup
soup = BeautifulSoup(page.text, 'html.parser')

# initialisation de la variable qui va contenir
# la liste de toutes les données des restaurants
restaurants = []

# scraping the home page
scrape_page(soup, restaurants)

# getting the "Next →" HTML element
next_li_element = soup.find('li', class_='next')


# création du fichier "NYRestaurants.csv"
csv_file = open('NYRestaurants.csv', 'w', encoding='utf-8', newline='')

# initialisation de l'insertion de données
# dans le fichier CSV
writer = csv.writer(csv_file)

# écriture de l'en-tête du fichier CSV
writer.writerow(['Nom du restaurant', 'Tags', 'Adresse', 'Ville', 'Numéro de tél'])

# écriture dans chaque ligne correspondant à un restaurant
for restaurant in restaurants:
    writer.writerow(restaurant.values())

# fin de l'écriture et fermeture du fichier CSV
csv_file.close()