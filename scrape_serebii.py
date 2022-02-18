import logging
from collections import defaultdict
from random import randint
from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')


def scrape_attackdex(
        save_csv: bool = True,
        file_path: str = 'data/attackdex.csv'
) -> pd.DataFrame:
    """Return dataframe of scraped item data from serebii.net"""
    gen_dict = {
        1: '-rby',
        2: '-gs',
        3: '',
        4: '-dp',
        5: '-bw',
        6: '-xy',
        7: '-sm',
        8: '-swsh'
    }
    type_list = [
        'bug',
        'dragon',
        'electric',
        'fighting',
        'fire',
        'flying',
        'ghost',
        'grass',
        'ground',
        'ice',
        'normal',
        'poison',
        'psychic',
        'rock',
        'water',
        'dark',
        'steel',
        'fairy'
    ]
    url = 'https://www.serebii.net/attackdex{site}/{prefix}{type_}.shtml'
    pokedict = defaultdict(list)
    all_headers = ['name', 'type', 'cat', 'pp', 'att', 'acc', 'effect', 'con_type']
    for gen, site in gen_dict.items():
        logging.info(f'Grabbing attackdex data for Generation {gen}...')
        prefix = 'type/' if gen <= 2 else ''
        if gen == 1:
            types = type_list[0:15]
        elif gen < 6:
            types = type_list[0:17]
        else:
            types = type_list
        for type_ in types:
            if type_ == 'psychic' and gen >= 3:
                type_ = 'psychict'  # Later convention to separate from the attack 'Psychic'
            r = requests.get(url.format(site=site, prefix=prefix, type_=type_)).text
            soup = BeautifulSoup(r, 'lxml')
            # Tables for only Gen 3 step away from the 'dextable' class convention
            table = soup.find('table', class_='dextable') if gen != 3 else soup.find_all('table')[4]
            headers = []
            for i, row in enumerate(table.find_all('tr')):
                if i == 0:
                    for cell in row.find_all('td'):
                        headers.append(cell.text.strip().lower().replace('.', '').replace(' ', '_'))
                else:
                    pokedict['generation'].append(gen)
                    pokedict['href'].append(row.a['href'].strip())
                    for header, cell in zip(headers, row.find_all('td')):
                        try:
                            pokedict[header].append(cell.img['src'].strip())
                        except TypeError:
                            pokedict[header].append(cell.text.strip())
                    empty_headers = [x for x in all_headers if x not in headers]
                    for empty in empty_headers:
                        pokedict[empty].append(None)
            sleep(randint(0, 3))
    pokedf = pd.DataFrame(data=pokedict)
    logging.info('Success! Data acquired.')
    if save_csv:
        pokedf.to_csv(file_path)
        logging.info(f'Saved attackdex data to {file_path}')
    return pokedf


if __name__ == '__main__':
    scrape_attackdex()
