import requests
from bs4 import BeautifulSoup
import json


def get_author_info(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    born_date = soup.find('span', class_='author-born-date').text.strip()
    born_location = soup.find('span', class_='author-born-location').text.strip()
    description = soup.find('div', class_='author-description').text.strip()

    return born_date, born_location, description


def get_quotes_and_authors(url):
    quotes = []
    authors = []

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for quote in soup.find_all('div', class_='quote'):
            text = quote.find('span', class_='text').text.strip()
            author_name = quote.find('small', class_='author').text.strip()
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]

            quotes.append({'quote': text, 'author': author_name, 'tags': tags})
            author_element = quote.find('span', class_='')
            if author_element:
                author_url = author_element.find('a')['href']
                born_date, born_location, description = get_author_info('http://quotes.toscrape.com' + author_url)
                authors.append({
                    'fullname': author_name,
                    'born_date': born_date,
                    'born_location': born_location,
                    'description': description
                })

        next_button = soup.find('li', class_='next')
        if next_button:
            url = base_url + next_button.find('a')['href']
        else:
            url = None

    return quotes, authors


def save_quotes(quotes):
    with open('quotes.json', 'w', encoding='utf-8') as file:
        json.dump(quotes, file, ensure_ascii=False, indent=4)


def save_authors(authors):
    with open('authors.json', 'w', encoding='utf-8') as file:
        json.dump(authors, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    base_url = 'http://quotes.toscrape.com'
    quotes, authors = get_quotes_and_authors(base_url)
    save_quotes(quotes)
    save_authors(authors)
