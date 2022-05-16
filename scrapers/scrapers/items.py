# Define here the models for your scraped items
#
# See documentation in:
# https://docs.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags


def strip(value: str) -> str:
    return value.strip()


class PokedexItem(Item):
    name = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    desc = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    img = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    pokedex_data = Field()
    training = Field()
    breeding = Field()
    base_stats = Field()
    pokedex_entries = Field()
    location = Field()
    languages = Field()
    name_origin = Field()
    type_defense = Field()


class MoveItem(Item):
    name = Field(input_processor=MapCompose(remove_tags, strip), output_processor=TakeFirst())
    move_target = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    move_data = Field()
    machine_record = Field()
    languages = Field()
    game_desc = Field()
    learnt_level = Field()
    learnt_prev = Field()
    learnt_breeding = Field()
    learnt_tr = Field()
    learnt_tm = Field()


class NaturesItem(Item):
    name = Field()
    increases = Field()
    decreases = Field()
