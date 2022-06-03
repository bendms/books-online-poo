from bs4 import BeautifulSoup
import requests
import csv
"""
##### FONCTION POUR FAIRE UNE REQUETE GET POUR OBTENIR LE CODE HTML DE LA PAGE #####

def make_the_soup(url_livre):
    # url_website = url_livre
    html_livre = requests.get(url_livre).text
    soup = BeautifulSoup(html_livre, 'html.parser')
    return soup

##### FONCTION POUR SCRAPER LA PAGE D'UN LIVRE #####

def scrap_my_book (url_livre, soup):
    #Pour chaque URL de liste livre, utiliser BeautifulSoup pour extraire les données et les stocker dans les listes
    tableau_livre = []
    html_livre = requests.get(url_livre).text
    soup_livre = BeautifulSoup(html_livre, 'html.parser')

    #URL Livre 
    product_page_url = url_livre

    #Title
    title = soup_livre.find(class_="col-sm-6 product_main")
    title = title.find('h1').string

    #Category
    list_a = []
    for a_href in soup_livre.find_all("a"):
        list_a.append(a_href.string)
    category = list_a[3]
    

    #Description
    description_class_search = soup_livre.find(class_="product_page")
    children_product_page = description_class_search.findChildren('p', recursive = False)
    description_livre_clean_tag = str(children_product_page).replace("<p>", "")
    product_description = str(description_livre_clean_tag).replace("</p>", "")

    #Review_rating 
    review_livre = soup_livre.find(class_="col-sm-6 product_main")
    children_review_livre = review_livre.find(class_="star-rating", recursive = False)
    children_review_livre.clear()
    children_review_livre_2 = str(children_review_livre).replace('<p class="star-rating ', "")
    review_rating = children_review_livre_2.replace('"></p>', "")

    #Extraction des données du tableau (UPC, Price excluding taxe, Price including tax, Number available)
    for td in soup_livre.find_all('td'):
        tableau_livre.append(td.string)
    universal_product_code = tableau_livre[0]
    price_excluding_tax = tableau_livre[2]
    price_including_tax = tableau_livre[3]
    number_available = tableau_livre[5]

    #Extraction de l'URL de l'image
    image_livre = soup.select("div img")
    image_url = url_livre + image_livre[0]["src"]
    download_image = requests.get(image_url).content
    with open("test_img.jpg", "wb") as handler:
        handler.write(download_image)

    informations_livre = [product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, product_description, category, review_rating, image_url]
    
    return informations_livre, category


##### FONCTION POUR CREER UN FICHIER CSV AVEC LE NOM DE LA CATEGORIE, Y AJOUTER LES ENTETES ET ECRIRE LES INFORMATIONS DANS LE FICHIER ###

def write_in_csv (category, informations_livre):
    
    file_name = str(category)
    #Créer une liste avec les entêtes suivantes : [”product_page_url”, “universal_ product_code (upc)”, “title, price_including_tax”, “price_excluding_tax”, “product_description”, “category”, “review_rating”, “image_url”]
    liste_csv = []
    entetes = ["product_page_url", "universal_product_code (upc)", "title", "price_including_tax", "price_excluding_tax", "product_description", "category", "review_rating", "image_url"]
    
    #Ouvrir un fichier CSV, y importer les entêtes et les informations dans des colonnes différentes
    with open(file_name + '.csv', 'w', encoding='UTF-8') as f:
        writer = csv.writer(f)
        liste_csv.append(entetes)
        liste_csv.append(informations_livre)
        writer.writerows(liste_csv)
    #Enregistrer et fermer le fichier CSV
 

url_livre = "https://books.toscrape.com/catalogue/soumission_998/index.html"
soup = make_the_soup(url_livre)
informations_livre  = scrap_my_book(url_livre, soup)[0]
category = scrap_my_book(url_livre,soup)[1]
write_in_csv(category, informations_livre)
"""


urls = []
for link in soup.find_all('a'):
    #print(link.get('href'))
    urls.append(link)
print(urls)

list = soup.find_all(class_="table table-striped")
print(list)

# Récupérer toutes les URL des produits via BeautifulSoup 
# Faire une requête Get pour obtenir le code HTML des pages suivantes si il y a

# Récupérez toutes les URL des pages suivantes de la catégorie
# Stocker les URL dans une liste (liste_livre)

#Récupération de tous les liens

links = []

#À partir d’une URL, faire une requête Get pour obtenir le code HTML de la page

url = "https://books.toscrape.com/catalogue/category/books/fiction_10/index.html"
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

# # Pour chaque élement de la liste (liste_livre), récupérer la page HTML
# # Créer les liste suivantes :

# - product_pageurl
# - universal product_code (upc)
# - title
# - price_including_tax
# - price_excluding_tax
# - number_available
# - product_description
# - category
# - review_rating
# - image_url






