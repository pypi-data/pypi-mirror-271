from functools import reduce


def unique(lst: list[str]) -> list[str]:
    empty = []  # type: list[str]
    return list(reduce(lambda acc, x: acc if x in acc else [*acc, x], lst, empty))


def flatten(ignore: list[str | list[str]]) -> list[str]:
    return list(sum(map(lambda x: x if isinstance(x, list) else [x], ignore), []))
