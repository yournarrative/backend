from random import choice
from string import ascii_lowercase


def generate_random_string(length: int = 16) -> str:
    return (''.join(choice(ascii_lowercase) for i in range(length)))
