# Define here the models for your scraped items
#
# See documentation in:
# https://docs.org/en/latest/topics/items.html

from typing import Union

from itemloaders.processors import Join, MapCompose, TakeFirst
from scrapy.item import Field, Item
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags


def strip(value: str) -> str:
    return value.strip()


def cast_int(value: str) -> Union[int, str]:
    try:
        x = int(value)
    except ValueError:
        return value
    else:
        return x


class PokemonItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class PokedexItem(Item):
    name = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    desc = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    img = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    pokedex_data = Field(output_processor=TakeFirst())
    training = Field(output_processor=TakeFirst())
    breeding = Field(output_processor=TakeFirst())
    base_stats = Field(output_processor=TakeFirst())
    pokedex_entries = Field(output_processor=TakeFirst())
    location = Field(output_processor=TakeFirst())
    languages = Field(output_processor=TakeFirst())
    name_origin = Field(output_processor=TakeFirst())
    type_defense = Field(output_processor=TakeFirst())


class MoveItem(Item):
    name = Field(input_processor=MapCompose(remove_tags, strip), output_processor=TakeFirst())
    move_target = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    move_data = Field(output_processor=TakeFirst())
    machine_record = Field(output_processor=TakeFirst())
    languages = Field(output_processor=TakeFirst())
    game_desc = Field(output_processor=TakeFirst())
    learnt_level = Field(output_processor=TakeFirst())
    learnt_prev = Field(output_processor=TakeFirst())
    learnt_breeding = Field(output_processor=TakeFirst())
    learnt_tr = Field(output_processor=TakeFirst())
    learnt_tm = Field(output_processor=TakeFirst())


class EggGroupItem(Item):
    egg_group = Field(input_processor=MapCompose(remove_tags, strip), output_processor=TakeFirst())
    img = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    number = Field(input_processor=MapCompose(remove_tags, cast_int), output_processor=TakeFirst())
    name = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    alt_name = Field(input_processor=MapCompose(remove_tags, strip), output_processor=TakeFirst())
    type = Field(input_processor=MapCompose(remove_tags, strip), output_processor=TakeFirst())
    other_group = Field(input_processor=MapCompose(remove_tags, strip), output_processor=TakeFirst())


class AbilityItem(Item):
    name = Field(input_processor=MapCompose(strip), output_processor=TakeFirst())
    effect = Field(input_processor=MapCompose(remove_tags), output_processor=Join())
    languages = Field(output_processor=TakeFirst())
    game_desc = Field(output_processor=TakeFirst())
    with_ability = Field(output_processor=TakeFirst())
    hidden_ability = Field(output_processor=TakeFirst())


class NaturesItem(Item):
    name = Field(input_processor=MapCompose(remove_tags, strip), output_processor=TakeFirst())
    increases = Field(input_processor=MapCompose(remove_tags, strip), output_processor=TakeFirst())
    decreases = Field(input_processor=MapCompose(remove_tags, strip), output_processor=TakeFirst())


class EVItem(Item):
    name = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    alt_name = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    img = Field(output_processor=TakeFirst())
    number = Field(input_processor=MapCompose(remove_tags, cast_int), output_processor=TakeFirst())
    hp = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    attack = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    defense = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    sp_atk = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    sp_def = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    speed = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())


class ItemItem(Item):
    name = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    img = Field(output_processor=TakeFirst())
    category = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    effect = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
