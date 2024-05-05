from .exit_if_empty import exit_if_empty
from .print_colorize import print_colorize
from .input_char import input_char
from .get_by_index import get_by_index




def print_choices(l):
    for i, v in enumerate(l):
        print(f"{i}. {v}")


def get_choices(prompt):
    print_colorize(prompt, text_end="")
    i = input_char()
    print()
    return i


def filter_choices(contains, daftar):
    if contains.isdigit():
        daftar = get_by_index(daftar, int(contains))
    else:
        daftar = [v for v in daftar if contains in v]
        if len(daftar) == 1:
            daftar = get_by_index(daftar, 0)
    return daftar


def get_contains(daftar, prompt):
    print_choices(daftar)
    contains = get_choices(prompt)
    exit_if_empty(len(contains))
    return contains


def choices(daftar, contains=None, prompt="Choose : "):
    """
    Memudahkan dalam membuat pilihan untuk user dalam tampilan console

    ```py
    var = {
        "Pertama" : "Pilihan Pertama",
        "Kedua" : "Pilihan Kedua",
        "Ketiga" : "Pilihan Ketiga",
    }
    res = choices(
        var,
        prompt="Pilih dari dictionary : "
    )
    print(res)
    ```
    """
    daftar = list(v for v in daftar)
    while isinstance(daftar, list):
        contains = contains or get_contains(daftar, prompt)
        daftar = filter_choices(contains, daftar)
        exit_if_empty(daftar)
        contains = None if contains != daftar else daftar
    return daftar
