from collections import defaultdict

import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrape_pokemon(save_csv: bool = True) -> pd.DataFrame:
    """Return dataframe of National Pokédex information scraped from pokemondb.net"""
    # TODO: error checks, adding logging
    url = 'https://pokemondb.net/pokedex/all'
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'lxml')
    rows = soup.find_all('tr')
    pokedict = defaultdict(list)
    stat_cols = ['number', 'hp', 'attack', 'defense', 'sp_atk', 'sp_def', 'speed']
    for i, row in enumerate(rows):
        if i == 0:
            pass
        else:
            alt_name = row.find('small', class_='text-muted')
            pokedict['name'].append(row.a.text.strip())
            pokedict['alt_name'].append(alt_name.text.strip() if alt_name else None)
            pokedict['href'].append(row.a['href'].strip())
            pokedict['sprite'].append(row.find('span', class_='img-fixed')['data-src'].strip())
            pokedict['total'].append(int(row.find('td', class_='cell-total').text.strip()))
            cellnums = row.find_all('td', attrs={'class': 'cell-num'})
            for idx, col in zip(range(len(stat_cols)), stat_cols):
                pokedict[col].append(int(cellnums[idx].text.strip()))
            types = row.find_all('a', class_='type-icon')
            for idx, type_ in enumerate(types):
                pokedict[f'type{idx+1}'].append(type_.text.strip())
                if idx == 0 and len(types) == 1:
                    pokedict[f'type2'].append(None)
    pokedf = pd.DataFrame(data=pokedict)
    if save_csv:
        pokedf.to_csv('data/pokemon.csv')
    return pokedf


if __name__ == '__main__':
    scrape_pokemon()
