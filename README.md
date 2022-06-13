# BOOKS SCRAPER

![BOOKS SCRAPER](https://user-images.githubusercontent.com/97233634/172905149-f35b2750-b665-455b-83f2-75ae0957a392.png)


## Review : 

This is my first Python project for OpenClassRooms courses. 

In this scenario we work for an online library and we need to create a script which scan and extract a competitor website to find informations about their books. 

This script will automatically scan their website from an URL. Find all the categories, find all the books in these categories and create a CSV file for each of them. 

Also, this script will download all cover pictures in .jpg format. 

## Installation : 

This script needs Python installed and some packages detailled in requirements.txt. 

1. Clone the repo with your terminal 

```bash
git clone https://github.com/bendms/books-online.git
```

## Configuration : 

1. Install packages from requirements.txt
```bash
pip install -r requirements.txt 
```
2. Run the script using Python commande in terminal : 
```bash
python main.py
```

3. You can use the 'time' command if you want to know how long the program takes to run
```bash
time python main.py
```   

## How to Contribute

This script takes time to be executed. It would be interesting to find a way to improve the execution speed : 

- Use multithreading
- Use LXML or CSS attribute to find HTML tags



