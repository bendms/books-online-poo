from bs4 import BeautifulSoup
import requests
import csv

#À partir d’une URL, faire une requête Get pour obtenir le code HTML de la page
#Faire une requête Get pour obtenir le code HTML de la page 1

url_website = "http://books.toscrape.com/"
html_website = requests.get(url_website).text
soup = BeautifulSoup(html_website, 'html.parser')

"""
urls = []
for link in soup.find_all('a'):
    #print(link.get('href'))
    urls.append(link)
print(urls)

list = soup.find_all(class_="table table-striped")
print(list)

Récupérer toutes les URL des produits via BeautifulSoup 
Faire une requête Get pour obtenir le code HTML des pages suivantes si il y a

Récupérez toutes les URL des pages suivantes de la catégorie
Stocker les URL dans une liste (liste_livre)

#Récupération de tous les liens

links = []

#À partir d’une URL, faire une requête Get pour obtenir le code HTML de la page

url = 
page = requests.get(url)
i = 0

while page.ok:
    page = requests.get(url)
    #Parcourir la page
    soup = BeautifulSoup(page.text, 'html.parser')
    product_pods = soup.find_all(class_="product_pod")
    for product_pod in product_pods:
        a = product_pod.find("a")
        link = a["href"]
        links.append("https://books.toscrape.com/catalogue/" + link + "\n")
        with open('liste_livres.txt', 'w', encoding='UTF-8') as f:
            writer = csv.writer(f)
            writer.writerow(links)
    print("Scraping des liens en cours ... \n page " + str(i))
    url = "http://books.toscrape.com/catalogue/page-" + str(i) + ".html" 
    i = i + 1

Pour chaque élement de la liste (liste_livre), récupérer la page HTML
Créer les liste suivantes :

- product_pageurl
- universal product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url
"""

product_page_url = []
universal_product_code = []
title = []
price_including_tax = []
price_excluding_tax = []
number_available = []
product_description = []
category = []
review_rating = []
image_url = []

#Pour chaque URL de liste livre, utiliser BeautifulSoup pour extraire les données et les stocker dans les listes

tableau_livre = []
url_livre = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
product_page_url.append(url_livre)
html_livre = requests.get(url_livre).text
soup_livre = BeautifulSoup(html_livre, 'html.parser')

#Title
title_livre = soup_livre.find(class_="col-sm-6 product_main")
title_livre = title_livre.find('h1').string
title.append(title_livre)

#Category #TODO: Retirer les retours à la ligne['\nPoetry\n']
category_livre = soup_livre.find(class_="breadcrumb")
li_livre = category_livre.find_all("li")
category.append(li_livre[2].text)

#Description TODO : Retirer les balises <p> </p>
description_livre = soup_livre.find(class_="product_page")
children_product_page = description_livre.findChildren('p', recursive = False)
product_description.append(children_product_page)

#Review_rating TODO : Retirer les balises <p class='star-rating ...>
review_livre = soup_livre.find(class_="col-sm-6 product_main")
children_review_livre = review_livre.find(class_="star-rating Three", recursive = False)
children_review_livre.clear()
review_rating.append(children_review_livre)

#Extraction des données du tableau
for td in soup_livre.find_all('td'):
    tableau_livre.append(td.string)

universal_product_code.append(tableau_livre[0])
price_excluding_tax.append(tableau_livre[2])
price_including_tax.append(tableau_livre[3])
number_available.append(tableau_livre[5])

#Extraction de l'URL de l'image
image_livre = soup.select("div img")
url_image_livre = url_website + image_livre[0]["src"]
image_url.append(url_image_livre)
download_image = requests.get(url_image_livre).content
with open("test_img.jpg", "wb") as handler:
    handler.write(download_image)

#Créer une liste avec les entêtes suivantes : [”product_page_url”, “universal_ product_code (upc)”, “title, price_including_tax”, “price_excluding_tax”, “product_description”, “category”, “review_rating”, “image_url”]
liste_entetes = ["product_page_url", "universal_ product_code (upc)", "title, price_including_tax", "price_excluding_tax", "product_description", "category", "review_rating", "image_url"]


#Ouvrir un fichier CSV et y importer les informations dans des colonnes différentes
with open('livre_info.csv', 'w', encoding='UTF-8') as f:
    writer = csv.writer(f)
    liste_entetes.append(product_page_url)
    liste_entetes.append(universal_product_code)
    liste_entetes.append(title)
    liste_entetes.append(price_including_tax)
    liste_entetes.append(price_excluding_tax)
    liste_entetes.append(number_available)
    liste_entetes.append(product_description)
    liste_entetes.append(category)
    liste_entetes.append(review_rating)
    liste_entetes.append(image_url)
    writer.writerow(liste_entetes)
#Enregistrer et fermer le fichier CSV
