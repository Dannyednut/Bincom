from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import requests

"""
1. Scrape books from All products | Books to Scrape - Sandbox
"""
driver = webdriver.Chrome()

books = []

# Scrape the first 5 pages
for page in range(1, 6):
    url = f"http://books.toscrape.com/catalogue/page-{page}.html"
    driver.get(url)

    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    book_items = soup.find_all('article', class_='product_pod')

    # Scrapping each book item
    for book_item in book_items:
        # Get the book URL
        book_url = "http://books.toscrape.com/catalogue/" + book_item.find('h3').find('a')['href']

        driver.get(book_url)

        time.sleep(2)

        book_soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Getting the book data
        book_data = {
            'Name': book_soup.find('div', class_='col-sm-6 product_main').find('h1').text.strip(),
            'Price': book_soup.find('p', class_='price_color').text.strip(),
            'Stock Status': book_soup.find('p', class_='instock availability').text.strip(),
            'Rating': book_soup.find('p', class_='star-rating')['class'][1],
            'Description': book_soup.find('div', id='product_description').find_next_sibling('p').text.strip() if book_soup.find('div', id='product_description') else '',
            'Product Information': [tr.text.strip() for tr in book_soup.find('table', class_='table table-striped').find_all('tr')],
            'Category': book_soup.find('ul', class_='breadcrumb').find_all('li')[-2].text.strip()
        }

        books.append(book_data)

driver.quit()

df = pd.DataFrame(books)

print(df)

"""
2. Scrape 10-20 distinct quote authors from Quotes to Scrape (Name, nationality, description, date of birth)
"""

details =[]
length = len(details)
authors = []
page = 1

while length < 10:
    url = f'https://quotes.toscrape.com/page/{page}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    items = soup.find_all('div', class_='quote')

    for item in items:
        about = item.find_all('span')
        about_url = "https://quotes.toscrape.com/" + about[1].find('a')['href']
        
        about_response = requests.get(about_url)
        about_soup = BeautifulSoup(about_response.content, 'html.parser')
      
        name = about_soup.find('h3', class_ = 'author-title').text.strip()

        about_data = {
            "Name": name,
            "Nationality": about_soup.find('span', class_='author-born-location').text.split(',')[-1].strip(),
            "Date-of-birth": about_soup.find('span', class_='author-born-date').text.strip(),
            "Description": about_soup.find('div', class_='author-description').text.strip()
        }

        if name not in authors:
            details.append(about_data)
            authors.append(name)

        length = len(details)
        if length == 10:
            break
        
    page+=1
    
# Convert the list to a pandas DataFrame
df = pd.DataFrame(details)

# Print the DataFrame
print(df)

"""
3. Build a scraper that will scrape a random page from Wikipedia
"""
import requests
from bs4 import BeautifulSoup

response = requests.get("https://en.wikipedia.org/wiki/Special:Random")

soup = BeautifulSoup(response.text, 'html.parser')

title = soup.find('h1', id='firstHeading').text
print(f"Title: {title}")

paragraphs = soup.find_all('p')
for paragraph in paragraphs:
    print(paragraph.text)

links = soup.find_all('a')
for link in links:
    print(link.get('href'))