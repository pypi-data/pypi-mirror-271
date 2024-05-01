from .chr_to_int import chr_to_int
from .int_to_chr import int_to_chr


def int_range(start, stop, step, index, number):
    start = int_int(start)
    stop = int_int(stop)
    step = fix_step(start, stop, step)
    for i in range(start, stop, step):
        yield i


def oct_range(start, stop, step, index, number):
    start = oct_oct(start)
    stop = oct_oct(stop)
    step = fix_step(start, stop, step)
    for i in range(start, stop, step):
        yield oct(i)


def hex_range(start, stop, step, index, number):
    start = hex_hex(start)
    stop = hex_hex(stop)
    step = fix_step(start, stop, step)
    for i in range(start, stop, step):
        yield hex(i)


def bin_range(start, stop, step, index, number):
    start = bin_bin(start)
    stop = bin_bin(stop)
    step = fix_step(start, stop, step)
    for i in range(start, stop, step):
        yield bin(i)


def chr_range(start, stop, step, index, numbers):
    start = chr_chr(start, index, numbers)
    stop = chr_chr(stop, index, numbers)
    step = fix_step(start, stop, step)
    for i in range(start, stop, step):
        yield int_to_chr(i, start=index, numbers=numbers)


irange_numbers = [
    (int_range, "0123456789"),
    (chr_range, "abcdefghijklmnopqrstuvwxyz"),
    (chr_range, "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    (bin_range, "01"),
    (oct_range, "01234567"),
    (hex_range, "0123456789abcdef"),
    (hex_range, "0123456789ABCDEF"),
]


def irange(start, stop=None, step=None, index=0, numbers=None):
    """
    Meningkatkan fungsi range() dari python untuk pengulangan menggunakan huruf

    ```python
    print(irange(10))
    print(irange(3, 15))
    iprint(irange(13, 5))
    iprint(irange(2, 10, 3))
    iprint(irange(2, '10', 3))
    iprint(irange('10'))
    iprint(irange('10', '100', 7))
    iprint(irange("h"))
    iprint(irange("A", "D"))
    iprint(irange("z", "a", 4))
    ```
    """
    start, stop, step = fix_args_position(start, stop, step)

    if numbers is not None:
        return chr_range(start, stop, step, index, numbers)

    start = str(start) if start is not None else ""
    stop = str(stop) if stop is not None else ""
    ss = set(start) | set(stop)
    for f, n in irange_numbers:
        for s in ss:
            if s not in n:
                break
        else:
            return f(start, stop, step, index, n)

    raise Exception("start dan stop tidak diketahui")


def bin_bin(start):
    return int(start, 2) if start else 0


def hex_hex(start):
    return int(start, 16) if start else 0


def oct_oct(start):
    return int(start, 8) if start else 0


def int_int(start):
    return int(start) if start else 0


def chr_chr(start, index, numbers):
    start = str(start) if start else numbers[0]
    start = chr_to_int(start, start=index, numbers=numbers)
    return start


def fix_args_position(start, stop, step):
    step = 1 if step is None else int(step)
    if stop is None:
        stop = start
        start = None
    return start, stop, step


def fix_step(start, stop, step):
    step = abs(step)
    if stop < start:
        step = step * -1
    return step
