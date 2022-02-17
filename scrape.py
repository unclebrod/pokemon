import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_pokemon(save: bool = True) -> pd.DataFrame:
    """Scrape pokemondb.net for basic Pokémon information"""
    # TODO: Differentiate between regular Pokémon and Mega/Alolan/etc., error checks
    url = 'https://pokemondb.net/pokedex/all'
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'lxml')
    rows = soup.find_all('tr')
    pokedict = {}
    list_cols = ['Type1', 'Type2', 'Sprite', 'href', 'Sprite']
    stat_cols = ['#', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
    for i, row in enumerate(rows):
        if i == 0:  #
            for header in row.find_all('div', class_='sortwrap'):
                # Headers include #, Name, Type, Total, HP, Attack, Defense, Sp. Atk, Sp. Def, & Speed
                pokedict[header.text.strip()] = []
            pokedict['Type1'] = pokedict.pop('Type')
            for col in list_cols:
                pokedict[col] = []
        else:
            pokedict['href'].append(row.a['href'].strip())
            pokedict['Sprite'].append(row.find('span', class_='img-fixed')['data-src'].strip())
            pokedict['Name'].append(row.a.text.strip())
            pokedict['Total'].append(int(row.find('td', class_='cell-total').text.strip()))
            cellnums = row.find_all('td', attrs={'class': 'cell-num'})
            for idx, col in zip(range(len(stat_cols)), stat_cols):
                pokedict[col].append(int(cellnums[idx].text.strip()))
            types = row.find_all('a', class_='type-icon')
            for idx, type_ in enumerate(types):
                pokedict[f'Type{idx+1}'].append(type_.text.strip())
                if idx == 0 and len(types) == 1:
                    pokedict[f'Type2'].append(None)
    pokedf = pd.DataFrame(data=pokedict)
    if save:
        pokedf.to_csv('pokemon')
    return pokedf


if __name__ == '__main__':
    scrape_pokemon()
