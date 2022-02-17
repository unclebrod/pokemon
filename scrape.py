import requests
from bs4 import BeautifulSoup

url = 'https://pokemondb.net/pokedex/all'
r = requests.get(url).text
soup = BeautifulSoup(r, 'lxml')
print(soup.prettify())