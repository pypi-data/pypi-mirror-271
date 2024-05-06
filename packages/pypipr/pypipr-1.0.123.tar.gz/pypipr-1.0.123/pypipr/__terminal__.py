from pypipr import *

def main():
    ppp = __import__("pypipr")
    m = ivars(ppp)
    # m = m["module"] | m["variable"] | m["class"] | m["function"]
    m = m["variable"] | m["function"]
    m = [x for x in m]
    m.sort()

    a = iargv(1)
    p = "Masukan Nomor Urut atau Nama Fungsi : "
    m = choices(daftar=m, contains=a, prompt=p)

    f = getattr(ppp, m)

    if a != m:
        print_colorize(m)
        print(f.__doc__)

    if inspect.isclass(f):
        print_log("Class tidak dapat dijalankan.")
    elif inspect.ismodule(f):
        print_log("Module tidak dapat dijalankan.")
    elif inspect.isfunction(f):
        s = inspect.signature(f)

        if not a:
            print(m, end="")
            print_colorize(s)

        k = {}
        for i, v in s.parameters.items():
            print(f"{i} [{v.default}] : ", end="")
            o = input()
            if len(o):
                try:
                    k[i] = eval(o)
                except Exception:
                    print_colorize(
                        "Input harus dalam syntax python.",
                        color=colorama.Fore.RED,
                    )

        f = f(**k)
    else:
        # variable
        pass

    iprint(f)


if __name__ == "__main__":
    main()
