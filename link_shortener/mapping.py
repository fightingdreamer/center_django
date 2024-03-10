import random

numbers = "23456789"
letters_lower = "bcdfghjkmnpqrstvwxyz"
letters_upper = "BCDFGHJKMNPQRSTVWXYZ"

mapping = numbers + letters_lower + letters_upper
mapping_reverse_lookup = {character: nr for nr, character in enumerate(mapping)}


def encode(uid: int) -> str:
    if uid < 0:
        raise ValueError("id cannot be negative")
    characters = []
    accumulator = uid
    while accumulator > 0:
        character = mapping[accumulator % len(mapping)]
        characters.append(character)
        accumulator = accumulator // len(mapping)
    return "".join(reversed(characters))


def decode(name: str) -> int:
    uid = 0
    try:
        for character in name:
            uid = uid * len(mapping) + mapping_reverse_lookup[character]
    except KeyError:
        raise ValueError("invalid character in name")
    return uid


def get_random_character():
    return mapping[random.randint(0, len(mapping) - 1)]


def get_random_padding(size: int):
    return "".join(get_random_character() if nr else "_" for nr in range(size))


def get_simple_padding(size: int):
    return "".join(
        mapping[(nr * len(mapping) // 6) % len(mapping)] if nr else "_"
        for nr in range(size)
    )


def with_padding(name: str, size: int, randomize: bool):
    missing = max(0, size - len(name))
    if randomize:
        padding = get_random_padding(missing)
    else:
        padding = get_simple_padding(missing)
    return name + padding


def drop_padding(name: str):
    return name.split("_", maxsplit=1)[0]


def encode_with_padding(uid: int, size: int, randomize: bool) -> str:
    return with_padding(encode(uid), size, randomize)


def decode_drop_padding(name: str) -> int:
    return decode(drop_padding(name))
