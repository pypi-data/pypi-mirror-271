def print_to_last_line(text: str, latest=1, clear=True):
    """
    Melakukan print ke konsol tetapi akan menimpa baris terakhir.
    Berguna untuk memberikan progress secara interaktif.

    ```py
    c = input("masukkan apa saja : ")
    print_to_last_line(f"masukkan apa saja : {c} [ok]")
    ```
    """
    t = ""

    if latest:
        t += f"\033[{latest}A"

    # if append:
    #     t += "\033[10000C" 
    # else:
    #     # t += "\r"
    #     t += "\033[F"
    #     # if clear:
    #     #     t += "\033[K"

    if clear:
        t += "\033[K"

    t += text
    print(t)


if __name__ == "__main__":
    c = input("masukkan apa saja : ")
    print_to_last_line(f"masukkan apa saja : {c} [ok]")
    print(f"masukkan apa saja : ")
    print(f"masukkan apa saja : bsmsidoneoslwjsj ")
    print(f"masukkan apa saja : ")
    print_to_last_line(f"masukkan apa saja : {c} [ok]", latest=2, clear=False)
