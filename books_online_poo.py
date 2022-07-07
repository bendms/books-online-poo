from fileinput import filename
from unicodedata import category
from bs4 import BeautifulSoup
import requests
import csv
from urllib.parse import urljoin
import re
import os


class Category:
    def __init__(self, name="", url="", list_of_books=[], all_books_infos_for_this_category=[]):
        self.name = name
        self.url = url
        self.list_of_books = list_of_books
        self.all_books_infos_for_this_category = all_books_infos_for_this_category
        
    def extract_books_url(self):
        books_links = []
        page = requests.get(self.url)
        while page.ok:
            page = requests.get(self.url)
            # Parcourir la page
            soup = BeautifulSoup(page.text, 'html.parser')
            product_pods = soup.find_all(class_="product_pod")
            for product_pod in product_pods:
                a = product_pod.find("a")
                link = urljoin(self.url, a["href"])
                books_links.append(link)
            # next_page_content = Category.check_next_page(page)
                page_content = BeautifulSoup(page.text, "html.parser")
                next_link = page_content.find(class_="next")
                if next_link is not None:
                    for a in next_link.find_all("a", href=True):
                        next_page = a["href"]
                    next_page_content = str(next_page).replace('<a href="', "").replace('">next</a>', "")
                else:
                    next_page_content = "404"
                self.url = urljoin(self.url, next_page_content)
            print(self.url)
        print("Nombre de livre(s) trouvé(s) dans la catégorie : " + str(len(books_links)))
        return books_links
    
    
    def find_category_name(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser')
        self.name = soup.find("h1").get_text()
        return self.name


class Book:
    def __init__(self, url="", upc="", title="", price_with_tax="", price_without_tax="", description="", category="",
                 review_rating="", image_url="", informations_livre=[]):
        self.url = url
        self.upc = upc
        self.title = title
        self.price_with_tax = price_with_tax
        self.price_without_tax = price_without_tax
        self.description = description
        self.category = category
        self.review_rating = review_rating
        self.image_url = image_url
        self.informations_livre = informations_livre

    def extract_book_information(self):
        tableau_livre = []
        html_livre = requests.get(self.url).content
        soup_livre = BeautifulSoup(html_livre, 'html.parser')

        # Title
        self.title = soup_livre.find(class_="col-sm-6 product_main")
        self.title = self.title.find('h1').string
        self.title = str(self.title)

        # Category
        list_a = []
        for a_href in soup_livre.find_all("a"):
            list_a.append(a_href.string)
        self.category = list_a[3]

        # Description
        description_class_search = soup_livre.find(class_="product_page")
        children_product_page = description_class_search.findChildren('p', recursive=False)
        description_livre_clean_tag = str(children_product_page).replace("<p>", "")
        product_description_with_special_character = str(description_livre_clean_tag).replace("</p>", "")
        self.description = re.sub('[^\w \n\.]', '', product_description_with_special_character)

        # Review_rating
        review_livre = soup_livre.find(class_="col-sm-6 product_main")
        children_review_livre = review_livre.find(class_="star-rating", recursive=False)
        children_review_livre.clear()
        children_review_livre_2 = str(children_review_livre).replace('<p class="star-rating ', "")
        self.review_rating = children_review_livre_2.replace('"></p>', "")

        # Extraction des données du tableau (UPC, Price excluding taxe, Price including tax)
        for td in soup_livre.find_all('td'):
            tableau_livre.append(td.string)
        self.upc = tableau_livre[0]
        self.price_excluding_tax = tableau_livre[2].replace("Â", "")
        self.price_including_tax = tableau_livre[3].replace("Â", "")

        # Extraction du nombre de produits disponibles (Number available)
        check_number_available = soup_livre.find(class_="instock availability").getText()
        check_space_before_number_available = check_number_available.replace("\n\n    \n        ", "")
        self.number_available = check_space_before_number_available.replace("\n    \n", "")

        # Extraction de l'URL de l'image
        image_livre = soup_livre.select("div img")
        self.image_url = urljoin(self.url, image_livre[0]["src"])
        download_image = requests.get(self.image_url).content

        self.informations_livre = [self.url, self.upc, self.title, self.price_including_tax, self.price_excluding_tax,
                              self.number_available, self.description, self.category, self.review_rating, self.image_url]

        name_my_image_without_special_characters = re.sub('[^\w \n\.]', '', self.title)

        if not os.path.exists("images"):
            os.makedirs("images")
        with open("images/" + name_my_image_without_special_characters + ".jpg", "wb+") as handler:
            handler.write(download_image)

        return self.informations_livre


class CsvFileMaker:
    def __init__(self, all_books_infos_for_this_category= []):
        self.all_books_infos_for_this_category = all_books_infos_for_this_category

    def create_and_write_in_csv(self, category_object, book_object):
        file_name = str(category_object.name)
        heading = ["product_page_url", "universal_product_code (upc)" , "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]

        liste_csv = []
        liste_csv.append(heading)
        for infos in self.all_books_infos_for_this_category:
            if file_name == book_object.category:
                liste_csv.append(infos)
        if not os.path.exists("datas"):
            os.makedirs("datas")
        with open("datas/" + file_name + '.csv', 'w', encoding='UTF-8', newline="") as f:
            writer = csv.writer(f)
            writer.writerows(liste_csv)   


def find_all_categories(url, page):
    list_of_categories_urls = []
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    nav_list = soup.find(class_="nav nav-list").find_all("a", href = True)
    for a in nav_list:
        a = urljoin(url, a["href"])
        list_of_categories_urls.append(a)
    list_of_categories_urls.pop(0)
    return list_of_categories_urls

def main(URL):
    # URL = "https://books.toscrape.com/"
    page = requests.get(URL, "html.parser")
    list_of_categories_urls = find_all_categories(URL, page)
    compteur_livre = 1
    i = 0
    for url_category in list_of_categories_urls:
        category_object = Category(url = url_category)
        category_object.name = category_object.find_category_name()
        category_object.list_of_books = category_object.extract_books_url()
        for book in category_object.list_of_books:
            book_object = Book(url = book)
            book_object.informations_livre = book_object.extract_book_information()
            category_object.all_books_infos_for_this_category.append(book_object.informations_livre)
            # print(all_books_informations)
            print(f"Scraping des livres en cours. Scraping {compteur_livre}/1000")
            compteur_livre += 1
        print(category_object.all_books_infos_for_this_category)
        if category_object.name == book_object.category:
            csv_maker_object = CsvFileMaker(category_object.all_books_infos_for_this_category)
            csv_maker_object.create_and_write_in_csv(category_object=category_object, book_object=book_object)
            category_object.all_books_infos_for_this_category.clear()
