from collections import defaultdict
from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrape_attackdex(save_csv: bool = True) -> pd.DataFrame:
    """Return dataframe of scraped item data from serebii.net"""
    # TODO: crawl across all generations, add logging
    types = [
        'bug', 'dragon', 'electric',
        'fighting', 'fire', 'flying',
        'ghost', 'grass', 'ground',
        'ice', 'normal', 'poison',
        'psychic', 'rock', 'water'
    ]
    url = 'https://www.serebii.net/attackdex-rby/type/{type_}.shtml'
    pokedict = defaultdict(list)
    fooinfo_cols = ['name', 'effect']
    cen_cols = ['pp', 'att', 'acc']
    for type_ in types:
        r = requests.get(url.format(type_=type_)).text
        soup = BeautifulSoup(r, 'lxml')
        table = soup.find('table', class_='dextable')
        for i, row in enumerate(table.find_all('tr')):
            if i == 0:
                pass
            else:
                pokedict['type'].append(type_)
                for cell, col in zip(row.find_all('td', class_='fooinfo'), fooinfo_cols):
                    pokedict[col].append(cell.text.strip())
                pokedict['href'].append(row.a['href'].strip())
                for idx, cell in enumerate(row.find_all('td', class_='cen')):
                    if idx == 0:
                        pokedict['img_src'].append(cell.img['src'].strip())
                    else:
                        val = cell.text.strip()
                        pokedict[cen_cols[idx-1]].append(None if val == '--' else float(val))
        sleep(1)
    pokedf = pd.DataFrame(data=pokedict)
    if save_csv:
        pokedf.to_csv('data/attackdex.csv')
    return pokedf


if __name__ == '__main__':
    scrape_attackdex()
