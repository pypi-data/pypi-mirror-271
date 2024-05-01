import random


def random_bool():
    """
    Menghasilkan nilai random True atau False.
    Fungsi ini merupakan fungsi tercepat untuk mendapatkan random bool.
    Fungsi ini sangat cepat, tetapi pemanggilan fungsi ini membutuhkan
    overhead yg besar.

    ```python
    print(random_bool())
    ```
    """
    return bool(random.getrandbits(1))

