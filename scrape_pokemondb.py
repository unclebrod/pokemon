import logging
from collections import defaultdict

import pandas as pd
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')


def scrape_pokemon(
        save_csv: bool = True,
        file_path: str = 'data/pokemon.csv'
) -> pd.DataFrame:
    """Return dataframe of National Pokédex information scraped from pokemondb.net"""
    url = 'https://pokemondb.net/pokedex/all'
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'lxml')
    rows = soup.find_all('tr')
    pokedict = defaultdict(list)
    headers = []
    logging.info('Grabbing national pokedex data from serebii...')
    for i, row in enumerate(rows):
        if i == 0:
            for cell in row.find_all('th'):
                headers.append(cell.text.strip().lower().replace('.', '').replace(' ', '_'))
        else:
            alt_name = row.find('small', class_='text-muted')
            pokedict['alt_name'].append(alt_name.text.strip() if alt_name else None)
            pokedict['href'].append(row.a['href'].strip())
            pokedict['sprite'].append(row.find('span', class_='img-fixed')['data-src'].strip())
            for header, cell in zip(headers, row.find_all('td')):
                val = cell.text.strip()
                if header == 'type':
                    types = val.split()
                    pokedict['type1'].append(types[0])
                    try:
                        pokedict['type2'].append(types[1])
                    except IndexError:
                        pokedict['type2'].append(None)
                else:
                    try:
                        pokedict[header].append(int(val))
                    except ValueError:
                        pokedict[header].append(val)
    pokedf = pd.DataFrame(data=pokedict)
    logging.info('Success! Data acquired.')
    if save_csv:
        pokedf.to_csv(file_path)
        logging.info(f'Saved attackdex data to {file_path}')
    return pokedf


if __name__ == '__main__':
    scrape_pokemon()
