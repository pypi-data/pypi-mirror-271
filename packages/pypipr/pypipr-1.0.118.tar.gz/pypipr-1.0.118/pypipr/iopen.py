import re
import urllib.request

import lxml.html

from .is_valid_url import is_valid_url
from .to_str import to_str


def iopen(path, data=None, regex=None, css_select=None, xpath=None, file_append=False):
    """
    Membaca atau Tulis pada path yang bisa merupakan FILE maupun URL.

    Baca File :
    - Membaca seluruh file.
    - Jika berhasil content dapat diparse dengan regex.
    - Apabila File berupa html, dapat diparse dengan css atau xpath.

    Tulis File :
    - Menulis pada file.
    - Jika file tidak ada maka akan dibuat.
    - Jika file memiliki content maka akan di overwrite.

    Membaca URL :
    - Mengakses URL dan mengembalikan isi html nya berupa teks.
    - Content dapat diparse dengan regex, css atau xpath.

    Tulis URL :
    - Mengirimkan data dengan metode POST ke url.
    - Jika berhasil dan response memiliki content, maka dapat diparse
      dengan regex, css atau xpath.


    ```python
    # FILE
    print(iopen("__iopen.txt", "mana aja"))
    print(iopen("__iopen.txt", regex="(\w+)"))
    # URL
    print(iopen("https://www.google.com/", css_select="a"))
    print(iopen("https://www.google.com/", dict(coba="dulu"), xpath="//a"))
    ```
    """
    path = to_str(path)
    content = ""

    if is_valid_url(path):
        req = dict(
            url=path,
            headers={
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 "
                "Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/108.0.0.0 Mobile Safari/537.36"
            },
        )

        if data:
            req["data"] = urllib.parse.urlencode(data).encode()

        req = urllib.request.Request(**req)

        # Connect to URL
        try:
            with urllib.request.urlopen(req) as url_open:
                content = url_open.read().decode()
        except Exception:
            # print(f"An error occurred: {str(e)}")
            return False

    else:
        # Write File
        if data is not None:
            mode = "a" if file_append else "w"
            with open(path, mode, encoding="utf-8") as f:
                content = f.write(data)
        # Read File
        else:
            try:
                with open(path, "r") as f:
                    content = f.read()
            except Exception:
                # print(f"An error occurred: {str(e)}")
                return False

    """ Parse """
    if regex:
        return re.findall(regex, content)
    if css_select:
        return lxml.html.fromstring(content).cssselect(css_select)
    if xpath:
        return lxml.html.fromstring(content).xpath(xpath)

    """ Return """
    return content


if __name__ == "__main__":
    from .iargv import iargv

    if filename := iargv(1):
        print(iopen(filename, iargv(2)))
