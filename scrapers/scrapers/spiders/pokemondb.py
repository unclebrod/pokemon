from unicodedata import normalize

from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule, Spider
from w3lib.html import remove_tags

from scrapers.items import EVItem, MoveItem, NaturesItem, PokedexItem

EGG_GROUPS = [
    "Amorphous",
    "Bug",
    "Dragon",
    "Fairy",
    "Field",
    "Flying",
    "Grass",
    "Human-Like",
    "Mineral",
    "Monster",
    "Water 1",
    "Water 2",
    "Water 3",
    "Ditto",
    "Undiscovered",
]


class PokedexSpider(CrawlSpider):
    # TODO: Consider alternatives to storing data in jsons - would db be better?
    # TODO: https://pypi.org/project/scrapy-fake-useragent/
    # TODO: Search for data discrepencies and clean up crawling
    name = "pokedex"
    allowed_domains = ["pokemondb.net"]
    start_urls = ["https://pokemondb.net/pokedex/all/"]
    rules = (
        Rule(
            LinkExtractor(allow="pokedex", deny=["national", "game"]),
            callback="parse_pokedex",
        ),
    )

    def parse_pokedex(self, response):
        page = response.url.split("/")[-1]
        filename = f"html/pokemondb/pokedex/{page}.html"
        with open(filename, "wb") as f:
            f.write(response.body)

        loader = ItemLoader(item=PokedexItem(), response=response)
        loader.add_css("name", "h1")
        loader.add_css("desc", "p")
        loader.add_css("img", "img::attr(src)")

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

        vitals_tables = response.css("table.vitals-table")

        if len(vitals_tables) >= 1:
            pokedex_table = vitals_tables[0]
            pokedex_keys = pokedex_table.css("th::text").getall()
            pokedex_vals = [
                normalize("NFKC", BeautifulSoup(x, "lxml").get_text().strip())
                for x in pokedex_table.css("td").getall()
            ]
            loader.add_value("pokedex_data", dict(zip(pokedex_keys, pokedex_vals)))

        if len(vitals_tables) >= 2:
            training_table = vitals_tables[1]
            training_keys = [remove_tags(x) for x in training_table.css("th").getall()]
            training_vals = [
                remove_tags(x).strip() for x in training_table.css("td").getall()
            ]
            loader.add_value("training", dict(zip(training_keys, training_vals)))

        if len(vitals_tables) >= 3:
            breeding_table = vitals_tables[2]
            breeding_keys = [remove_tags(x) for x in breeding_table.css("th").getall()]
            breeding_vals = [
                remove_tags(x).strip() for x in breeding_table.css("td").getall()
            ]
            loader.add_value("breeding", dict(zip(breeding_keys, breeding_vals)))

        if len(vitals_tables) >= 4:
            base_stats_table = vitals_tables[3]
            base_stats_keys = base_stats_table.css("th::text").getall()
            base_stats_vals = base_stats_table.css("td.cell-num::text").getall()[::3]
            loader.add_value("base_stats", dict(zip(base_stats_keys, base_stats_vals)))

        if len(vitals_tables) >= 5:
            pokedex_entries_table = vitals_tables[4]
            pokedex_entries_keys = [
                remove_tags(x) for x in pokedex_entries_table.css("th").getall()
            ]
            pokedex_entries_vals = pokedex_entries_table.css("td::text").getall()
            loader.add_value(
                "pokedex_entries", dict(zip(pokedex_entries_keys, pokedex_entries_vals))
            )

        if len(vitals_tables) >= 6:
            where_to_find_table = vitals_tables[5]
            where_to_find_keys = [
                remove_tags(x) for x in where_to_find_table.css("th").getall()
            ]
            where_to_find_vals = [
                remove_tags(x) for x in where_to_find_table.css("td").getall()
            ]
            loader.add_value(
                "location", dict(zip(where_to_find_keys, where_to_find_vals))
            )

        if len(vitals_tables) >= 7:
            other_languages_table = vitals_tables[6]
            other_languages_keys = other_languages_table.css("th::text").getall()
            other_languages_vals = other_languages_table.css("td::text").getall()
            loader.add_value(
                "languages", dict(zip(other_languages_keys, other_languages_vals))
            )

        yield loader.load_item()


class MovesSpider(CrawlSpider):
    name = "moves"
    allowed_domains = ["pokemondb.net"]
    start_urls = ["https://pokemondb.net/move/all"]
    rules = (
        Rule(LinkExtractor(allow="move", deny=["mechanics"]), callback="parse_moves"),
    )

    def parse_moves(self, response):
        page = response.url.split("/")[-1]
        filename = f"html/pokemondb/move/{page}.html"
        with open(filename, "wb") as f:
            f.write(response.body)

        loader = ItemLoader(item=MoveItem(), response=response)
        loader.add_css("name", "h1")
        loader.add_css("move_target", "p.mt-descr")

        vitals_tables = response.css("table.vitals-table")
        move_data_table = vitals_tables[0]

        if len(vitals_tables) == 4:
            machine_record_table = vitals_tables[1]
            other_languages_table = vitals_tables[2]
            game_desc_table = vitals_tables[3]
        else:
            machine_record_table = None
            other_languages_table = vitals_tables[1]
            game_desc_table = vitals_tables[2]

        move_data_keys = move_data_table.css("th::text").getall()
        move_data_vals = [
            normalize("NFKC", BeautifulSoup(x, "lxml").get_text().strip())
            for x in move_data_table.css("td").getall()
        ]
        loader.add_value("move_data", dict(zip(move_data_keys, move_data_vals)))

        if machine_record_table is not None:
            machine_record_keys = [
                remove_tags(x.encode("ascii", "ignore"))
                for x in machine_record_table.css("th").getall()
            ]

            machine_record_vals = [
                remove_tags(x) for x in machine_record_table.css("td").getall()
            ]
            loader.add_value(
                "machine_record", dict(zip(machine_record_keys, machine_record_vals))
            )

        other_languages_keys = other_languages_table.css("th::text").getall()
        other_languages_vals = other_languages_table.css("td::text").getall()
        loader.add_value(
            "languages", dict(zip(other_languages_keys, other_languages_vals))
        )

        game_desc_keys = [
            remove_tags(x.encode("ascii", "ignore"))
            for x in response.css("table.vitals-table")[2].css("th").getall()
        ]
        game_desc_vals = game_desc_table.css("td::text").getall()
        loader.add_value("game_desc", dict(zip(game_desc_keys, game_desc_vals)))

        learnt_tables = response.css("div.infocard-list.infocard-list-pkmn-md")
        for table in learnt_tables:
            names = table.css("a.ent-name::text").getall()
            values = [remove_tags(x) for x in table.css("small.text-muted").getall()]
            if any("Level" in value for value in values):
                levels = [x for x in values if "Level" in x]
                loader.add_value("learnt_level", dict(zip(names, levels)))
            elif any("Gen" in value for value in values):
                gens = [x for x in values if "Gen" in x]
                loader.add_value("learnt_prev", dict(zip(names, gens)))
            elif response.css("h2#move-egg").get():
                null_vals = ["#", "Galarian", "Alolan"]
                groups = [
                    x
                    for x in values
                    if any(y in x for y in EGG_GROUPS)
                    and not any(y in x for y in null_vals)
                ]
                loader.add_value("learnt_breeding", dict(zip(names, groups)))
            elif response.css("h2#move-tr").get():
                loader.add_value("learnt_tr", names)
            else:
                loader.add_value("learnt_tm", names)

        yield loader.load_item()


class NaturesSpider(Spider):
    name = "natures"
    allowed_domains = ["pokemondb.net"]
    start_urls = ["https://pokemondb.net/mechanics/natures"]

    def parse(self, response):
        filename = f"html/pokemondb/natures/natures.html"
        with open(filename, "wb") as f:
            f.write(response.body)

        natures_table = response.css("tbody")[1]
        for row in natures_table.css("tr"):
            loader = ItemLoader(item=NaturesItem(), selector=row)
            loader.add_css("name", "td.ent-name")
            loader.add_css("increases", "td.text-positive")
            loader.add_css("decreases", "td.text-negative")

            yield loader.load_item()


class EVSpider(Spider):
    name = "ev"
    allowed_domains = ["pokemondb.net"]
    start_urls = ["https://pokemondb.net/ev/all"]

    def parse(self, response):
        filename = f"html/pokemondb/ev/ev.html"
        with open(filename, "wb") as f:
            f.write(response.body)

        ev_table = response.css("tbody")
        for row in ev_table.css("tr"):
            loader = ItemLoader(item=EVItem(), selector=row)
            cells = row.css("td")
            loader.add_value("img", cells[0].css("span::attr(data-src)").get())
            loader.add_value("number", cells[0].css("span.infocard-cell-data").get())
            loader.add_value("name", cells[1].css("a.ent-name").get())
            loader.add_value("alt_name", cells[1].css("small.text-muted").get())
            loader.add_value("hp", cells[2].css("td").get())
            loader.add_value("attack", cells[3].css("td").get())
            loader.add_value("defense", cells[4].css("td").get())
            loader.add_value("sp_atk", cells[5].css("td").get())
            loader.add_value("sp_def", cells[6].css("td").get())
            loader.add_value("speed", cells[7].css("td").get())

            yield loader.load_item()
