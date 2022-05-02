from unicodedata import normalize

from bs4 import BeautifulSoup
from scrapers.items import PokemonDBItem
from scrapy import Spider
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags


class PokemonDBSpider(Spider):
    # TODO: use CrawlSpider for additional functionality
    name = "pokemondb"
    allowed_domains = ["www.pokemondb.net"]
    start_urls = ["https://pokemondb.net/pokedex/bulbasaur/"]

    def parse(self, response, **kwargs):
        page = response.url.split("/")[-2]
        filename = f"html/pokemondb-{page}.html"
        with open(filename, "wb") as f:
            f.write(response.body)

        loader = ItemLoader(item=PokemonDBItem(), response=response)
        loader.add_css("name", "h1")
        loader.add_css("desc", "p")
        loader.add_css("img", "img::attr(src)")
        tables = response.css("table.vitals-table")

        pokedex_table = tables[0]
        pokedex_keys = pokedex_table.css("th::text").getall()
        pokedex_vals = [
            normalize("NFKC", BeautifulSoup(x, "lxml").get_text().strip())
            for x in tables[0].css("td").getall()
        ]
        loader.add_value("pokedex_data", dict(zip(pokedex_keys, pokedex_vals)))

        training_table = tables[1]
        training_keys = [remove_tags(x) for x in training_table.css("th").getall()]
        training_vals = [
            remove_tags(x).strip() for x in training_table.css("td").getall()
        ]
        loader.add_value("training", dict(zip(training_keys, training_vals)))

        breeding_table = tables[2]
        breeding_keys = [remove_tags(x) for x in breeding_table.css("th").getall()]
        breeding_vals = [
            remove_tags(x).strip() for x in breeding_table.css("td").getall()
        ]
        loader.add_value("breeding", dict(zip(breeding_keys, breeding_vals)))

        base_stats_table = tables[3]
        base_stats_keys = base_stats_table.css("th::text").getall()
        base_stats_vals = base_stats_table.css("td.cell-num::text").getall()[::3]
        loader.add_value("base_stats", dict(zip(base_stats_keys, base_stats_vals)))

        pokedex_entries_table = tables[4]
        pokedex_entries_keys = [
            remove_tags(x) for x in pokedex_entries_table.css("th").getall()
        ]
        pokedex_entries_vals = pokedex_entries_table.css("td::text").getall()
        loader.add_value(
            "pokedex_entries", dict(zip(pokedex_entries_keys, pokedex_entries_vals))
        )

        where_to_find_table = tables[5]
        where_to_find_keys = [
            remove_tags(x) for x in where_to_find_table.css("th").getall()
        ]
        where_to_find_vals = [
            remove_tags(x) for x in where_to_find_table.css("td").getall()
        ]
        loader.add_value("location", dict(zip(where_to_find_keys, where_to_find_vals)))

        other_languages_table = tables[6]
        other_languages_keys = other_languages_table.css("th::text").getall()
        other_languages_vals = other_languages_table.css("td::text").getall()
        loader.add_value(
            "languages", dict(zip(other_languages_keys, other_languages_vals))
        )

        name_origin_table = response.css("dl.etymology")
        name_origin_keys = name_origin_table.css("dt::text").getall()
        name_origin_vals = name_origin_table.css("dd::text").getall()
        loader.add_value("name_origin", dict(zip(name_origin_keys, name_origin_vals)))

        type_defenses_table = response.css("div.resp-scroll.text-center")
        type_defenses_keys = (
            type_defenses_table.css("th").css("a::attr(title)").getall()
        )
        type_defenses_vals = [
            remove_tags(x) for x in type_defenses_table.css("td").getall()
        ]
        loader.add_value(
            "type_defense", dict(zip(type_defenses_keys, type_defenses_vals))
        )

        yield loader.load_item()

        # next_page = response.css("a.entity-nav-next").attrib["href"]
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield response.follow(next_page, callback=self.parse)
