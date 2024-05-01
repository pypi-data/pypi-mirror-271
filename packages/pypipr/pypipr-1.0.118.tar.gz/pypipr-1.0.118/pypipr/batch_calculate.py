from .batchmaker import batchmaker
from .calculate import calculate


def batch_calculate(pattern):
    """
    Analisa perhitungan massal.
    Bisa digunakan untuk mencari alternatif terendah/tertinggi/dsb.


    ```python
    print(batch_calculate("{1 10} m ** {1 3}"))
    print(list(batch_calculate("{1 10} m ** {1 3}")))
    ```
    """
    patterns = batchmaker(pattern)

    for i in patterns:
        try:
            yield (i, calculate(i))
        except Exception:
            yield (i, None)

    # c = None
    # for i in patterns:
    #     try:
    #         c = calculate(i)
    #     except Exception:
    #         c = None
    #     yield (i, c)


if __name__ == "__main__":
    from ..ifunctions.iargv import iargv
    from ..ifunctions.iprint import iprint

    if i := iargv(1):
        iprint(batch_calculate(i))
