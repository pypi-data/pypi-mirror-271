import random


def rand_port(_min: int = 30000, _max: int = 32767) -> int:
    return random.randint(_min, _max)
