import inspect

c = {
    "module": inspect.ismodule,
    "class": inspect.isclass,
    "method": inspect.ismethod,
    "function": inspect.isfunction,
}


def ivars(obj, skip_underscore=True):
    """
    Membuat dictionary berdasarkan kategori untuk setiap
    member dari object.

    ```python
    iprint(ivars(__import__('pypipr')))
    ```
    """
    r = {}
    for i, v in vars(obj).items():
        z = None

        for x, y in c.items():
            if y(v):
                z = x
                break
        else:
            z = "variable"
        # if z is None:
        #     z = "variable"
        # z = z or "variable"

        if i.startswith("__") or i.endswith("__"):
            if skip_underscore:
                continue
            z = f"__{z}__"

        r.setdefault(z, {})[i] = v
        # try:
        #     r[z][i] = v
        # except Exception:
        #     r[z] = {}
        #     r[z][i] = v

    return r

if __name__ == "__main__":
    print(ivars(__import__("pypipr")))
