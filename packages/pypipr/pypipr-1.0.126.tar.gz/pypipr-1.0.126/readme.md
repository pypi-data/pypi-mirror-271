
# About
The Python Package Index Project (pypipr)

pypi : https://pypi.org/project/pypipr


# Setup
Install with pip
```
pip install pypipr
```

Then import pypipr
```python
from pypipr import *
# or
import pypipr
```

Or run in terminal/console/cmd/bash
```cmd
pypipr
```

# CONSTANT

`LINUX`

`PintUreg`

`WINDOWS`

# FUNCTION

## avg

`avg(i)`

Simple Average Function karena tidak disediakan oleh python  
  
```python  
n = [1, 22, 2, 3, 13, 2, 123, 12, 31, 2, 2, 12, 2, 1]  
print(avg(n))  
```

Output:
```py
16.285714285714285
```

## get_filemtime

`get_filemtime(filename)`

Mengambil informasi last modification time file dalam nano seconds  
  
```python  
print(get_filemtime(__file__))  
```

Output:
```py
1714399678112897487
```

## print_colorize

`print_colorize(text, color='\x1b[32m', bright='\x1b[1m', color_end='\x1b[0m', text_start='', text_end='\n', delay=0.05)`

Print text dengan warna untuk menunjukan text penting  
  
```py  
print_colorize("Print some text")  
print_colorize("Print some text", color=colorama.Fore.RED)  
```

## print_log

`print_log(text)`

Akan melakukan print ke console.  
Berguna untuk memberikan informasi proses program yg sedang berjalan.  
  
```python  
print_log("Standalone Log")  
```

Output:
```py
[32m[1m>>> Standalone Log[0m
```

## console_run

`console_run(info, command=None, print_info=True, capture_output=False)`

Menjalankan command seperti menjalankan command di Command Terminal  
  
```py  
console_run('dir')  
console_run('ls')  
```

## auto_reload

`auto_reload(filename)`

Menjalankan file python secara berulang.  
Dengan tujuan untuk melihat perubahan secara langsung.  
Pastikan kode aman untuk dijalankan.  
Jalankan kode ini di terminal console.  
  
```py  
auto_reload("file_name.py")  
```  
  
or run in terminal  
  
```  
pypipr auto_reload  
```

## basename

`basename(path)`

Mengembalikan nama file dari path  
  
```python  
print(basename("/ini/nama/folder/ke/file.py"))  
```

Output:
```py
file.py
```

## chr_to_int

`chr_to_int(s, start=0, numbers='abcdefghijklmnopqrstuvwxyz')`

Fungsi ini berguna untuk mengubah urutan huruf menjadi angka.  
  
```python  
print(chr_to_int('z'))  # Output: 26  
print(chr_to_int('aa'))  # Output: 27  
print(chr_to_int('abc', numbers="abc"))  # Output: 18  
```

Output:
```py
25
26
17
```

## int_to_chr

`int_to_chr(n, start=0, numbers='abcdefghijklmnopqrstuvwxyz')`

Fungsi ini berguna untuk membuat urutan dari huruf.  
Seperti a, b, ...., z, aa, bb, ....  
  
```python  
for i in range(30):  
    print(f"{i} = {int_to_chr(i)}")  
  
print(int_to_chr(7777))  
```

Output:
```py
0 = a
1 = b
2 = c
3 = d
4 = e
5 = f
6 = g
7 = h
8 = i
9 = j
10 = k
11 = l
12 = m
13 = n
14 = o
15 = p
16 = q
17 = r
18 = s
19 = t
20 = u
21 = v
22 = w
23 = x
24 = y
25 = z
26 = aa
27 = ab
28 = ac
29 = ad
kmd
```

## irange

`irange(start, stop=None, step=None, index=0, numbers=None)`

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

Output:
```py
<generator object int_range at 0x7a10b00440>
<generator object int_range at 0x7a10b00440>
[13, 12, 11, 10, 9, 8, 7, 6]
[2, 5, 8]
[2, 5, 8]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
[10, 17, 24, 31, 38, 45, 52, 59, 66, 73, 80, 87, 94]
['a', 'b', 'c', 'd', 'e', 'f', 'g']
['A', 'B', 'C']
['z', 'v', 'r', 'n', 'j', 'f', 'b']
```

## batchmaker

`batchmaker(pattern: str)`

Alat Bantu untuk membuat teks yang berulang.  
Gunakan `{[start][separator][finish]([separator][step])}`.  
```  
[start] dan [finish]    -> bisa berupa huruf maupun angka  
([separator][step])     -> bersifat optional  
[separator]             -> selain huruf dan angka  
[step]                  -> berupa angka positif  
```  
  
```python  
s = "Urutan {1/6/3} dan {10:9} dan {j k} dan {Z - A - 15} saja."  
print(batchmaker(s))  
print(list(batchmaker(s)))  
```

Output:
```py
<generator object batchmaker at 0x7a10af8280>
['Urutan 1 dan 10 dan j dan Z saja.', 'Urutan 1 dan 10 dan j dan K saja.', 'Urutan 4 dan 10 dan j dan Z saja.', 'Urutan 4 dan 10 dan j dan K saja.']
```

## calculate

`calculate(teks)`

Mengembalikan hasil dari perhitungan teks menggunakan modul pint.  
Mendukung perhitungan matematika dasar dengan satuan.  
  
Return value:  
- Berupa class Quantity dari modul pint  
  
Format:  
- f"{result:~P}"            -> pretty  
- f"{result:~H}"            -> html  
- result.to_base_units()    -> SI  
- result.to_compact()       -> human readable  
  
```python  
fx = "3 meter * 10 cm * 3 km"  
res = calculate(fx)  
print(res)  
print(res.to_base_units())  
print(res.to_compact())  
print(f"{res:~P}")  
print(f"{res:~H}")  
```

Output:
```py
90 centimeter * kilometer * meter
900.0 meter ** 3
900.0 meter ** 3
90 cm·km·m
90 cm km m
```

## batch_calculate

`batch_calculate(pattern)`

Analisa perhitungan massal.  
Bisa digunakan untuk mencari alternatif terendah/tertinggi/dsb.  
  
  
```python  
print(batch_calculate("{1 10} m ** {1 3}"))  
print(list(batch_calculate("{1 10} m ** {1 3}")))  
```

Output:
```py
<generator object batch_calculate at 0x7a10a73010>
[('1 m ** 1', <Quantity(1, 'meter')>), ('1 m ** 2', <Quantity(1, 'meter ** 2')>), ('2 m ** 1', <Quantity(2, 'meter')>), ('2 m ** 2', <Quantity(2, 'meter ** 2')>), ('3 m ** 1', <Quantity(3, 'meter')>), ('3 m ** 2', <Quantity(3, 'meter ** 2')>), ('4 m ** 1', <Quantity(4, 'meter')>), ('4 m ** 2', <Quantity(4, 'meter ** 2')>), ('5 m ** 1', <Quantity(5, 'meter')>), ('5 m ** 2', <Quantity(5, 'meter ** 2')>), ('6 m ** 1', <Quantity(6, 'meter')>), ('6 m ** 2', <Quantity(6, 'meter ** 2')>), ('7 m ** 1', <Quantity(7, 'meter')>), ('7 m ** 2', <Quantity(7, 'meter ** 2')>), ('8 m ** 1', <Quantity(8, 'meter')>), ('8 m ** 2', <Quantity(8, 'meter ** 2')>), ('9 m ** 1', <Quantity(9, 'meter')>), ('9 m ** 2', <Quantity(9, 'meter ** 2')>)]
```

## bin_to_int

`bin_to_int(n)`

Fungsi ini berguna untuk mengubah angka binary  
menjadi angka integer.  
  
```python  
print(bin_to_int(bin(244)))  
```

Output:
```py
244
```

## is_empty

`is_empty(variable, empty=[None, False, 0, 0, '0', '', '-0', '\n', '\t', set(), {}, [], ()])`

Mengecek apakah variable setara dengan nilai kosong pada empty.  
  
Pengecekan nilai yang setara menggunakan simbol '==', sedangkan untuk  
pengecekan lokasi memory yang sama menggunakan keyword 'is'  
  
```python  
print(is_empty("teks"))  
print(is_empty(True))  
print(is_empty(False))  
print(is_empty(None))  
print(is_empty(0))  
print(is_empty([]))  
```

Output:
```py
False
False
True
True
True
True
```

## exit_if_empty

`exit_if_empty(*args)`

Keluar dari program apabila seluruh variabel  
setara dengan empty  
  
```py  
var1 = None  
var2 = '0'  
exit_if_empty(var1, var2)  
```

## input_char

`input_char(prompt=None, prompt_ending='', newline_after_input=True, echo_char=True, default=None, color=None)`

Meminta masukan satu huruf tanpa menekan Enter.  
  
```py  
input_char("Input char : ")  
input_char("Input char : ", default='Y')  
input_char("Input Char without print : ", echo_char=False)  
```

## get_by_index

`get_by_index(obj, index, on_error=None)`

Mendapatkan value dari object berdasarkan indexnya.  
Jika error out of range maka akan mengembalikan on_error.  
  
```python  
l = [1, 3, 5]  
print(get_by_index(l, 7))  
```

Output:
```py
None
```

## choices

`choices(daftar, contains=None, prompt='Choose : ')`

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

## chunk_array

`chunk_array(array, size, start=0)`

Membagi array menjadi potongan-potongan dengan besaran yg diinginkan  
  
```python  
arr = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]  
print(chunk_array(arr, 5))  
print(list(chunk_array(arr, 5)))  
```

Output:
```py
<generator object chunk_array at 0x7a10b00440>
[[2, 3, 12, 3, 3], [42, 42, 1, 43, 2], [42, 41, 4, 24, 32], [42, 3, 12, 32, 42], [42]]
```

## create_folder

`create_folder(folder_name)`

Membuat folder.  
Membuat folder secara recursive dengan permission.  
  
```py  
create_folder("contoh_membuat_folder")  
create_folder("contoh/membuat/folder/recursive")  
create_folder("./contoh_membuat_folder/secara/recursive")  
```

## datetime_from_string

`datetime_from_string(iso_string, timezone='UTC')`

Parse iso_string menjadi datetime object  
  
```python  
print(datetime_from_string("2022-12-12 15:40:13").isoformat())  
print(datetime_from_string(  
    "2022-12-12 15:40:13",  
    timezone="Asia/Jakarta"  
).isoformat())  
```

Output:
```py
2022-12-12T15:40:13+00:00
2022-12-12T15:40:13+07:00
```

## datetime_now

`datetime_now(timezone=None)`

Memudahkan dalam membuat Datetime untuk suatu timezone tertentu  
  
```python  
print(datetime_now("Asia/Jakarta"))  
print(datetime_now("GMT"))  
print(datetime_now("Etc/GMT+7"))  
```

Output:
```py
2024-05-06 17:58:05.473000+07:00
2024-05-06 10:58:05.475089+00:00
2024-05-06 03:58:05.482857-07:00
```

## dict_first

`dict_first(d: dict, remove=False)`

Mengambil nilai (key, value) pertama dari dictionary dalam bentuk tuple.  
  
```python  
d = {  
    "key2": "value2",  
    "key3": "value3",  
    "key1": "value1",  
}  
print(dict_first(d, remove=True))  
print(dict_first(d))  
```

Output:
```py
('key2', 'value2')
('key3', 'value3')
```

## dirname

`dirname(path)`

Mengembalikan nama folder dari path.  
Tanpa trailing slash di akhir.  
  
```python  
print(dirname("/ini/nama/folder/ke/file.py"))  
```

Output:
```py
/ini/nama/folder/ke
```

## is_iterable

`is_iterable(var, str_is_iterable=False)`

Mengecek apakah suatu variabel bisa dilakukan forloop atau tidak  
  
```python  
s = 'ini string'  
print(is_iterable(s))  
  
l = [12,21,2,1]  
print(is_iterable(l))  
  
r = range(100)  
print(is_iterable(r))  
  
d = {'a':1, 'b':2}  
print(is_iterable(d.values()))  
```

Output:
```py
False
True
True
True
```

## to_str

`to_str(value)`

Mengubah value menjadi string literal  
  
```python  
print(to_str(5))  
print(to_str([]))  
print(to_str(False))  
print(to_str(True))  
print(to_str(None))  
```

Output:
```py
5

False
True

```

## filter_empty

`filter_empty(iterable, zero_is_empty=True, str_strip=True)`

Mengembalikan iterabel yang hanya memiliki nilai  
  
```python  
var = [1, None, False, 0, "0", True, {}, ['eee']]  
print(filter_empty(var))  
iprint(filter_empty(var))  
```

Output:
```py
<generator object filter_empty at 0x7a10a715d0>
[1, '0', True, {}, ['eee']]
```

## get_class_method

`get_class_method(cls)`

Mengembalikan berupa tuple yg berisi list dari method dalam class  
  
```python  
class ExampleGetClassMethod:  
    def a():  
        return [x for x in range(10)]  
  
    def b():  
        return [x for x in range(10)]  
  
    def c():  
        return [x for x in range(10)]  
  
    def d():  
        return [x for x in range(10)]  
  
print(get_class_method(ExampleGetClassMethod))  
print(list(get_class_method(ExampleGetClassMethod)))  
```

Output:
```py
<generator object get_class_method at 0x7a10a732e0>
[<function ExampleGetClassMethod.a at 0x7a10b151c0>, <function ExampleGetClassMethod.b at 0x7a10b15080>, <function ExampleGetClassMethod.c at 0x7a10b15120>, <function ExampleGetClassMethod.d at 0x7a10b15260>]
```

## get_filesize

`get_filesize(filename)`

Mengambil informasi file size dalam bytes  
  
```python  
print(get_filesize(__file__))  
```

Output:
```py
465
```

## github_init

`github_init()`

Menyiapkan folder offline untuk dikoneksikan ke repository  
kosong github.  
Akan langsung di upload dan di taruh di branch main.  
  
  
```py  
github_init()  
```  
  
or run in terminal  
  
```py  
pypipr github_init  
```

## github_pull

`github_pull()`

Menjalankan command `git pull`  
  
```py  
github_pull()  
```

## github_push

`github_push(commit_msg=None)`

Menjalankan command status, add, commit dan push  
  
```py  
github_push('Commit Message')  
```

## github_user

`github_user(email=None, name=None)`

Menyimpan email dan nama user secara global sehingga tidak perlu  
menginput nya setiap saat.  
  
```py  
github_user('my@emil.com', 'MyName')  
```

## hex_to_int

`hex_to_int(n)`

Fungsi ini berguna untuk mengubah angka hexadecimal  
menjadi angka integer.  
  
```python  
print(hex_to_int(hex(244)))  
```

Output:
```py
244
```

## iargv

`iargv(key: int, cast=None, on_error=None)`

Mengambil parameter input dari terminal tanpa menimbulkan error  
apabila parameter kosong.  
Parameter yg berupa string juga dapat diubah menggunakan cast.  
  
```python  
print(iargv(1, cast=int, on_error=100))  
```

Output:
```py
100
```

## idumps_html

`idumps_html(data, indent=None)`

Serialisasi python variabel menjadi HTML.  
  
```html  
List -> <ul>...</ul>  
Dict -> <table>...</table>  
```  
  
```python  
data = {  
    'abc': 123,  
    'list': [1, 2, 3, 4, 5],  
    'dict': {'a': 1, 'b':2, 'c':3},  
}  
print(idumps_html(data))  
```

Output:
```py
<table>
  <tbody>
    <tr>
      <th>abc</th>
      <td>
        <span>123</span>
      </td>
    </tr>
    <tr>
      <th>list</th>
      <td>
        <ul>
          <li>
            <span>1</span>
          </li>
          <li>
            <span>2</span>
          </li>
          <li>
            <span>3</span>
          </li>
          <li>
            <span>4</span>
          </li>
          <li>
            <span>5</span>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <th>dict</th>
      <td>
        <table>
          <tbody>
            <tr>
              <th>a</th>
              <td>
                <span>1</span>
              </td>
            </tr>
            <tr>
              <th>b</th>
              <td>
                <span>2</span>
              </td>
            </tr>
            <tr>
              <th>c</th>
              <td>
                <span>3</span>
              </td>
            </tr>
          </tbody>
        </table>
      </td>
    </tr>
  </tbody>
</table>

```

## idumps

`idumps(data, syntax='yaml', indent=4)`

Mengubah variabel data menjadi string untuk yang dapat dibaca untuk disimpan.  
String yang dihasilkan berbentuk syntax YAML/JSON/HTML.  
  
```python  
data = {  
    'a': 123,  
    't': ['disini', 'senang', 'disana', 'senang'],  
    'l': (12, 23, [12, 42]),  
}  
print(idumps(data))  
print(idumps(data, syntax='html'))  
```

Output:
```py
a: 123
l: !!python/tuple
- 12
- 23
-   - 12
    - 42
t:
- disini
- senang
- disana
- senang

<table>
    <tbody>
        <tr>
            <th>a</th>
            <td>
                <span>123</span>
            </td>
        </tr>
        <tr>
            <th>t</th>
            <td>
                <ul>
                    <li>
                        <span>disini</span>
                    </li>
                    <li>
                        <span>senang</span>
                    </li>
                    <li>
                        <span>disana</span>
                    </li>
                    <li>
                        <span>senang</span>
                    </li>
                </ul>
            </td>
        </tr>
        <tr>
            <th>l</th>
            <td>
                <ul>
                    <li>
                        <span>12</span>
                    </li>
                    <li>
                        <span>23</span>
                    </li>
                    <li>
                        <ul>
                            <li>
                                <span>12</span>
                            </li>
                            <li>
                                <span>42</span>
                            </li>
                        </ul>
                    </li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>

```

## int_to_int

`int_to_int(n)`

Fungsi ini sama seperti fungsi int().  
fungsi ini dibuat hanya untuk keperluan pembuatan module semata.  
  
```python  
print(int_to_int(7777))  
```

Output:
```py
7777
```

## ienumerate

`ienumerate(iterator, start=0, key=<function int_to_int at 0x7a19f09a80>)`

meningkatkan fungsi enumerate() pada python  
untuk key menggunakan huruf dan basis angka lainnya.  
  
```python  
it = ["ini", "contoh", "enumerator"]  
print(ienumerate(it))  
iprint(ienumerate(it, key=int_to_chr))  
```

Output:
```py
<generator object ienumerate at 0x7a10a733d0>
[('a', 'ini'), ('b', 'contoh'), ('c', 'enumerator')]
```

## ienv

`ienv(on_windows=None, on_linux=None)`

Mengambalikan hasil berdasarkan environment dimana program dijalankan  
  
```py  
getch = __import__(ienv(on_windows="msvcrt", on_linux="getch"))  
  
  
f = ienv(on_windows=fwin, on_linux=flin)  
f()  
  
  
inherit = ienv(  
    on_windows=[BaseForWindows, BaseEnv, object],  
    on_linux=[SpecialForLinux, BaseForLinux, BaseEnv, object]  
)  
  
class ExampleIEnv(*inherit):  
    pass  
```

## iexec

`iexec(python_syntax, import_pypipr=True)`

improve exec() python function untuk mendapatkan outputnya  
  
```python  
print(iexec('print(9*9)'))  
```

Output:
```py
81

```

## ijoin

`ijoin(iterable, separator='', start='', end='', remove_empty=False, recursive=True, recursive_flat=False, str_strip=False)`

Simplify Python join functions like PHP function.  
Iterable bisa berupa sets, tuple, list, dictionary.  
  
```python  
arr = {'asd','dfs','weq','qweqw'}  
print(ijoin(arr, ', '))  
  
arr = '/ini/path/seperti/url/'.split('/')  
print(ijoin(arr, ','))  
print(ijoin(arr, ',', remove_empty=True))  
  
arr = {'a':'satu', 'b':(12, 34, 56), 'c':'tiga', 'd':'empat'}  
print(ijoin(arr, separator='</li>\n<li>', start='<li>', end='</li>',  
    recursive_flat=True))  
print(ijoin(arr, separator='</div>\n<div>', start='<div>', end='</div>'))  
print(ijoin(10, ' '))  
```

Output:
```py
dfs, weq, qweqw, asd
,ini,path,seperti,url,
ini,path,seperti,url
<li>satu</li>
<li>12</li>
<li>34</li>
<li>56</li>
<li>tiga</li>
<li>empat</li>
<div>satu</div>
<div><div>12</div>
<div>34</div>
<div>56</div></div>
<div>tiga</div>
<div>empat</div>
10
```

## iloads_html

`iloads_html(html)`

Mengambil data yang berupa list `<ul>`, dan table `<table>` dari html  
dan menjadikannya data python berupa list.  
setiap data yang ditemukan akan dibungkus dengan tuple sebagai separator.  
  
```  
list (<ul>)     -> list         -> list satu dimensi  
table (<table>) -> list[list]   -> list satu dimensi didalam list  
```  
  
apabila data berupa ul maka dapat dicek type(data) -> html_ul  
apabila data berupa ol maka dapat dicek type(data) -> html_ol  
apabila data berupa dl maka dapat dicek type(data) -> html_dl  
apabila data berupa table maka dapat dicek type(data) -> html_table  
  
```python  
import pprint  
pprint.pprint(iloads_html(iopen("https://harga-emas.org/")), depth=10)  
pprint.pprint(iloads_html(iopen("https://harga-emas.org/1-gram/")), depth=10)  
```

Output:
```py
(['Home', 'Emas 1 Gram', 'History', 'Trend', 'Perak 1 Gram', 'Pluang'],
 [['Harga Emas Hari Ini - Senin, 06 Mei 2024'],
  ['Spot Emas USD↑2.319,91 (+17,34) / oz',
   'Kurs IDR↓16.094,00 (-108,00) / USD',
   'Emas IDR↑1.200.401 (+977) / gr'],
  ['LM Antam (Jual)↓1.310.000 (-3.000) / gr',
   'LM Antam (Beli)↓1.203.000 (-3.000) / gr']],
 [['Harga Emas Hari Ini'],
  ['Gram', 'Gedung Antam Jakarta', 'Pegadaian'],
  ['per Gram (Rp)', 'per Batangan (Rp)', 'per Gram (Rp)', 'per Batangan (Rp)'],
  ['1000',
   '1.251 (-3)',
   '1.250.600 (-3.000)',
   '1.043.040 (+8.200)',
   '1.043.040.000 (+8.200.000)'],
  ['500',
   '2.501 (-6)',
   '1.250.640 (-3.000)',
   '1.043.082 (+8.200)',
   '521.541.000 (+4.100.000)'],
  ['250',
   '5.004 (-12)',
   '1.251.060 (-3.000)',
   '1.043.512 (+8.200)',
   '260.878.000 (+2.050.000)'],
  ['100',
   '12.521 (-30)',
   '1.252.120 (-3.000)',
   '1.044.600 (+8.200)',
   '104.460.000 (+820.000)'],
  ['50',
   '25.058 (-60)',
   '1.252.900 (-3.000)',
   '1.045.400 (+8.200)',
   '52.270.000 (+410.000)'],
  ['25',
   '50.179 (-120)',
   '1.254.480 (-3.000)',
   '1.047.040 (+8.200)',
   '26.176.000 (+205.000)'],
  ['10',
   '125.950 (-300)',
   '1.259.500 (-3.000)',
   '1.052.200 (+8.200)',
   '10.522.000 (+82.000)'],
  ['5',
   '253.000 (-600)',
   '1.265.000 (-3.000)',
   '1.057.800 (+8.200)',
   '5.289.000 (+41.000)'],
  ['3',
   '423.889 (-1.000)',
   '1.271.667 (-3.000)',
   '1.064.667 (+8.000)',
   '3.194.000 (+24.000)'],
  ['2',
   '640.000 (-1.500)',
   '1.280.000 (-3.000)',
   '1.073.500 (+8.500)',
   '2.147.000 (+17.000)'],
  ['1',
   '1.310.000 (-3.000)',
   '1.310.000 (-3.000)',
   '1.104.000 (+8.000)',
   '1.104.000 (+8.000)'],
  ['0.5',
   '2.820.000 (-6.000)',
   '1.410.000 (-3.000)',
   '1.208.000 (+8.000)',
   '604.000 (+4.000)'],
  ['Update harga LM Antam :06 Mei 2024, pukul 08:30Harga pembelian kembali '
   ':Rp. 1.203.000/gram (-3.000)',
   'Update harga LM Pegadaian :31 Agustus 2023']],
 [['Spot Harga Emas Hari Ini (Market Open)'],
  ['Satuan', 'USD', 'Kurs\xa0Dollar', 'IDR'],
  ['Ounce\xa0(oz)', '2.319,91 (+17,34)', '16.094,00 (-108,00)', '37.336.632'],
  ['Gram\xa0(gr)', '74,59', '16.094,00', '1.200.401 (+977)'],
  ['Kilogram\xa0(kg)', '74.586,84', '16.094,00', '1.200.400.580'],
  ['Update harga emas :06 Mei 2024, pukul 17:58Update kurs :06 Mei 2024, pukul '
   '13:10']],
 [['Gram', 'UBS Gold 99.99%'],
  ['Jual', 'Beli'],
  ['/ Batang', '/ Gram', '/ Batang', '/ Gram'],
  ['100',
   '124.800.000 (-1.200.000)',
   '1.248.000 (-12.000)',
   '122.685.000 (-700.000)',
   '1.226.850 (-7.000)'],
  ['50',
   '62.500.000 (-450.000)',
   '1.250.000 (-9.000)',
   '61.395.000 (-350.000)',
   '1.227.900 (-7.000)'],
  ['25',
   '31.300.000 (-200.000)',
   '1.252.000 (-8.000)',
   '30.800.000 (-175.000)',
   '1.232.000 (-7.000)'],
  ['10',
   '12.570.000 (-80.000)',
   '1.257.000 (-8.000)',
   '12.370.000 (-70.000)',
   '1.237.000 (-7.000)'],
  ['5',
   '6.310.000 (-40.000)',
   '1.262.000 (-8.000)',
   '6.237.000 (-35.000)',
   '1.247.400 (-7.000)'],
  ['1',
   '1.310.000 (-5.000)',
   '1.310.000 (-5.000)',
   '1.280.000 (-7.000)',
   '1.280.000 (-7.000)'],
  ['', 'Update :06 Mei 2024, pukul 11:07']],
 [['Konversi Satuan'],
  ['Satuan', 'Ounce (oz)', 'Gram (gr)', 'Kilogram (kg)'],
  ['Ounce\xa0(oz)', '1', '31,1034767696', '0,0311034768'],
  ['Gram\xa0(gr)', '0,0321507466', '1', '0.001'],
  ['Kilogram\xa0(kg)', '32,1507466000', '1.000', '1']],
 [['Pergerakan Harga Emas Dunia'],
  ['Waktu', 'Emas'],
  ['Unit', 'USD', 'IDR'],
  ['Angka', '+/-', 'Angka', '+/-'],
  ['Hari Ini', 'Kurs', '', '', '16.202', '-108-0,67%'],
  ['oz', '2.302,57', '+17,34+0,75%', '37.306.239', '+30.392+0,08%'],
  ['gr', '74,03', '+0,56+0,75%', '1.199.423', '+977+0,08%'],
  ['30 Hari', 'Kurs', '', '', '15.907', '+187+1,18%'],
  ['oz', '2.329,93', '-10,02-0,43%', '37.062.197', '+274.435+0,74%'],
  ['gr', '74,91', '-0,32-0,43%', '1.191.577', '+8.823+0,74%'],
  ['2 Bulan', 'Kurs', '', '', '15.723', '+371+2,36%'],
  ['oz', '2.156,44', '+163,47+7,58%', '33.905.706', '+3.430.925+10,12%'],
  ['gr', '69,33', '+5,26+7,58', '1.090.094', '+110.307+10,12%'],
  ['6 Bulan', 'Kurs', '', '', '15.593', '+501+3,21%'],
  ['oz', '1.954,36', '+365,55+18,70%', '30.474.335', '+6.862.296+22,52%'],
  ['gr', '62,83', '+11,75+18,70%', '979.773', '+220.628+22,52%'],
  ['1 Tahun', 'Kurs', '', '', '15.731', '+363+2,31%'],
  ['oz', '1.823,86', '+496,05+27,20%', '28.691.142', '+8.645.490+30,13%'],
  ['gr', '58,64', '+15,95+27,20%', '922.442', '+277.959+30,13%'],
  ['2 Tahun', 'Kurs', '', '', '14.418', '+1.676+11,62%'],
  ['oz', '1.883,86', '+436,05+23,15%', '27.161.493', '+10.175.138+37,46%'],
  ['gr', '60,57', '+14,02+23,15%', '873.262', '+327.138+37,46%'],
  ['3 Tahun', 'Kurs', '', '', '14.364', '+1.730+12,04%'],
  ['oz', '1.831,48', '+488,43+26,67%', '26.307.379', '+11.029.253+41,92%'],
  ['gr', '58,88', '+15,70+26,67%', '845.802', '+354.599+41,92%'],
  ['5 Tahun', 'Kurs', '', '', '14.305', '+1.789+12,51%'],
  ['oz', '1.280,40', '+1.039,51+81,19%', '18.316.122', '+19.020.510+103,85%'],
  ['gr', '41,17', '+33,42+81,19%', '588.877', '+611.524+103,85%']])
(['Home', 'Emas 1 Gram', 'History', 'Trend', 'Perak 1 Gram', 'Pluang'],
 [[''],
  ['Emas 24 KaratHarga Emas 1 Gram', ''],
  ['USD', '74,59↑', '+0,56+0,76%'],
  ['KURS', '16.035,65↑', '+66,95+0,42%'],
  ['IDR', '1.196.048,44↑', '+13.896,04+1,18%'],
  ['Senin, 06 Mei 2024 17:58']],
 [[''],
  ['Emas 1 Gram (IDR)Emas 1 Gram (USD)Kurs USD-IDR',
   'Hari Ini',
   '1 Bulan',
   '1 Tahun',
   '5 Tahun',
   'Max',
   '']],
 [['Pergerakkan Harga Emas 1 Gram'],
  ['', 'Penutupan Kemarin', 'Pergerakkan Hari Ini', 'Rata-rata'],
  ['USD', '74,03', '74,03 - 74,59', '74,31'],
  ['KURS', '15.968,70', '15.968,70 - 16.035,65', '16.002,18'],
  ['IDR', '1.182.152,40', '1.182.152,40 - 1.196.048,44', '1.189.100,42'],
  [''],
  ['', 'Awal Tahun', 'Pergerakkan YTD', '+/- YTD'],
  ['USD', '66,32', '64,07 - 77,14', '+8,27 (12,47%)'],
  ['KURS', '15.390,10', '15.390,00 - 16.307,80', '+645,55 (4,19%)'],
  ['IDR', '1.020.729,53', '997.660,12 - 1.256.829,06', '+175.318,91 (17,18%)'],
  [''],
  ['', 'Tahun Lalu / 52 Minggu', 'Pergerakkan 52 Minggu', '+/- 52 Minggu'],
  ['USD', '64,87', '58,43 - 77,14', '+9,72 (14,98%)'],
  ['KURS', '14.669,40', '14.674,80 - 16.307,80', '+1.366,25 (9,31%)'],
  ['IDR', '951.626,36', '912.925,68 - 1.256.829,06', '+244.422,08 (25,68%)']])
```

## iloads

`iloads(data, syntax='yaml')`

Mengubah string data hasil dari idumps menjadi variabel.  
String data adalah berupa syntax YAML.  
  
```python  
data = {  
    'a': 123,  
    't': ['disini', 'senang', 'disana', 'senang'],  
    'l': (12, 23, [12, 42]),  
}  
s = idumps(data)  
print(iloads(s))  
```

Output:
```py
{'a': 123, 'l': (12, 23, [12, 42]), 't': ['disini', 'senang', 'disana', 'senang']}
```

## int_to_bin

`int_to_bin(n)`

Fungsi ini sama seperti fungsi bin().  
fungsi ini dibuat hanya untuk keperluan pembuatan module semata.  
  
```python  
print(int_to_bin(7777))  
```

Output:
```py
0b1111001100001
```

## int_to_hex

`int_to_hex(n)`

Fungsi ini sama seperti fungsi hex().  
fungsi ini dibuat hanya untuk keperluan pembuatan module semata.  
  
```python  
print(int_to_hex(7777))  
```

Output:
```py
0x1e61
```

## int_to_oct

`int_to_oct(n)`

Fungsi ini sama seperti fungsi oct().  
fungsi ini dibuat hanya untuk keperluan pembuatan module semata.  
  
```python  
print(int_to_oct(7777))  
```

Output:
```py
0o17141
```

## is_valid_url

`is_valid_url(path)`

Mengecek apakah path merupakan URL yang valid atau tidak.  
Cara ini merupakan cara yang paling efektif.  
  
```python  
print(is_valid_url("https://chat.openai.com/?model=text-davinci-002-render-sha"))  
print(is_valid_url("https://chat.openai.com/?model/=text-dav/inci-002-render-sha"))  
```

Output:
```py
True
True
```

## iopen

`iopen(path, data=None, regex=None, css_select=None, xpath=None, file_append=False)`

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

Output:
```py
8
['mana', 'aja']
[<Element a at 0x7a10b09810>, <Element a at 0x7a10b4d040>, <Element a at 0x7a10b4d0e0>, <Element a at 0x7a10b4d130>, <Element a at 0x7a10b4d180>, <Element a at 0x7a10b4d1d0>, <Element a at 0x7a10b4d220>, <Element a at 0x7a10b4d270>, <Element a at 0x7a10b4d2c0>, <Element a at 0x7a10b4d310>, <Element a at 0x7a10b4d360>, <Element a at 0x7a10b4d3b0>, <Element a at 0x7a10b4d400>, <Element a at 0x7a10b4d450>, <Element a at 0x7a10b4d4a0>, <Element a at 0x7a10b4d4f0>, <Element a at 0x7a10b4d540>, <Element a at 0x7a10b4d590>]
False
```

## iprint

`iprint(*args, color=None, sort_dicts=False, **kwargs)`

Improve print function dengan menambahkan color dan pretty print  
Color menggunakan colorama Fore + Back + Style  
  
```python  
import colorama  
iprint(  
    'yang ini',  
    {'12':12,'sdsd':{'12':21,'as':[88]}},  
    color=colorama.Fore.BLUE + colorama.Style.BRIGHT  
)  
```

Output:
```py
[34m[1myang ini[0m [34m[1m{'12': 12, 'sdsd': {'12': 21, 'as': [88]}}[0m
```

## ireplace

`ireplace(string: str, replacements: dict, flags=re.IGNORECASE|re.MULTILINE|re.DOTALL)`

STRing TRanslate mengubah string menggunakan kamus dari dict.  
Replacement dapat berupa text biasa ataupun regex pattern.  
Apabila replacement berupa regex, gunakan raw string `r"..."`  
Untuk regex capturing gunakan `(...)`, dan untuk mengaksesnya  
gunakan `\1`, `\2`, .., dst.  
  
```python  
text = 'aku ini mau ke sini'  
replacements = {  
    "sini": "situ",  
    r"(ini)": r"itu dan \1",  
}  
print(ireplace(text, replacements))  
```

Output:
```py
aku itu dan ini mau ke situ
```

## iscandir

`iscandir(folder_name='.', glob_pattern='*', recursive=True, scan_file=True, scan_folder=True)`

Mempermudah scandir untuk mengumpulkan folder dan file.  
  
```python  
print(iscandir())  
print(list(iscandir("./", recursive=False, scan_file=False)))  
```

Output:
```py
<generator object iscandir at 0x7a10b00740>
[PosixPath('.git'), PosixPath('.vscode'), PosixPath('pypipr'), PosixPath('__pycache__'), PosixPath('dist')]
```

## isplit

`isplit(text, separator='', include_separator=False)`

Memecah text menjadi list berdasarkan separator.  
  
```python  
t = '/ini/contoh/path/'  
print(isplit(t, separator='/'))  
```

Output:
```py
['', 'ini', 'contoh', 'path', '']
```

## ivars

`ivars(obj, skip_underscore=True)`

Membuat dictionary berdasarkan kategori untuk setiap  
member dari object.  
  
```python  
iprint(ivars(__import__('pypipr')))  
```

Output:
```py
{'class': {'APIMixinView': <class 'pypipr.APIMixinView.APIMixinView'>,
           'ComparePerformance': <class 'pypipr.ComparePerformance.ComparePerformance'>,
           'PintUregQuantity': <class 'pint.Quantity'>,
           'RunParallel': <class 'pypipr.RunParallel.RunParallel'>},
 'function': {'avg': <function avg at 0x7a1db6e700>,
              'get_filemtime': <function get_filemtime at 0x7a1a016de0>,
              'print_colorize': <function print_colorize at 0x7a1a016fc0>,
              'print_log': <function print_log at 0x7a1a0ceb60>,
              'console_run': <function console_run at 0x7a1a016e80>,
              'auto_reload': <function auto_reload at 0x7a19ff7ec0>,
              'basename': <function basename at 0x7a1a016d40>,
              'chr_to_int': <function chr_to_int at 0x7a1a017560>,
              'int_to_chr': <function int_to_chr at 0x7a1a017600>,
              'irange': <function irange at 0x7a1a017880>,
              'batchmaker': <function batchmaker at 0x7a1a017240>,
              'calculate': <function calculate at 0x7a1a017380>,
              'batch_calculate': <function batch_calculate at 0x7a1a017100>,
              'bin_to_int': <function bin_to_int at 0x7a1a0171a0>,
              'is_empty': <function is_empty at 0x7a19e38040>,
              'exit_if_empty': <function exit_if_empty at 0x7a1a017ec0>,
              'input_char': <function input_char at 0x7a1a017f60>,
              'get_by_index': <function get_by_index at 0x7a19e380e0>,
              'choices': <function choices at 0x7a19e382c0>,
              'chunk_array': <function chunk_array at 0x7a19e38360>,
              'create_folder': <function create_folder at 0x7a19e38400>,
              'datetime_from_string': <function datetime_from_string at 0x7a19e384a0>,
              'datetime_now': <function datetime_now at 0x7a19e38540>,
              'dict_first': <function dict_first at 0x7a19e385e0>,
              'dirname': <function dirname at 0x7a19e38680>,
              'is_iterable': <function is_iterable at 0x7a19e38860>,
              'to_str': <function to_str at 0x7a19e38900>,
              'filter_empty': <function filter_empty at 0x7a19e38720>,
              'get_class_method': <function get_class_method at 0x7a19e387c0>,
              'get_filesize': <function get_filesize at 0x7a19e38a40>,
              'github_init': <function github_init at 0x7a19e38b80>,
              'github_pull': <function github_pull at 0x7a19e38ae0>,
              'github_push': <function github_push at 0x7a19e38cc0>,
              'github_user': <function github_user at 0x7a19e38d60>,
              'hex_to_int': <function hex_to_int at 0x7a19e38e00>,
              'iargv': <function iargv at 0x7a19e38ea0>,
              'idumps_html': <function idumps_html at 0x7a19e39120>,
              'idumps': <function idumps at 0x7a19e38fe0>,
              'int_to_int': <function int_to_int at 0x7a19f09a80>,
              'ienumerate': <function ienumerate at 0x7a19e39620>,
              'ienv': <function ienv at 0x7a19e3b1a0>,
              'iexec': <function iexec at 0x7a19f09b20>,
              'ijoin': <function ijoin at 0x7a19f09c60>,
              'iloads_html': <function iloads_html at 0x7a19f09e40>,
              'iloads': <function iloads at 0x7a19f09bc0>,
              'int_to_bin': <function int_to_bin at 0x7a19f09da0>,
              'int_to_hex': <function int_to_hex at 0x7a19f09ee0>,
              'int_to_oct': <function int_to_oct at 0x7a19f09f80>,
              'is_valid_url': <function is_valid_url at 0x7a19f0a160>,
              'iopen': <function iopen at 0x7a19d125c0>,
              'iprint': <function iprint at 0x7a19f0a0c0>,
              'ireplace': <function ireplace at 0x7a19d12700>,
              'iscandir': <function iscandir at 0x7a19dc9d00>,
              'isplit': <function isplit at 0x7a19dc9da0>,
              'ivars': <function ivars at 0x7a19dc9e40>,
              'log': <function log at 0x7a19dc9ee0>,
              'oct_to_int': <function oct_to_int at 0x7a19dc9f80>,
              'password_generator': <function password_generator at 0x7a19dca020>,
              'pip_freeze_without_version': <function pip_freeze_without_version at 0x7a19dca160>,
              'poetry_publish': <function poetry_publish at 0x7a19dca200>,
              'poetry_update_version': <function poetry_update_version at 0x7a19dca340>,
              'print_dir': <function print_dir at 0x7a19dca520>,
              'print_to_last_line': <function print_to_last_line at 0x7a19dca5c0>,
              'random_bool': <function random_bool at 0x7a19dca660>,
              'restart': <function restart at 0x7a19dca700>,
              'set_timeout': <function set_timeout at 0x7a19dca7a0>,
              'sets_ordered': <function sets_ordered at 0x7a19dca840>,
              'str_cmp': <function str_cmp at 0x7a19dca8e0>,
              'text_colorize': <function text_colorize at 0x7a19dca980>},
 'variable': {'LINUX': True,
              'PintUreg': <pint.registry.UnitRegistry object at 0x7a1db70850>,
              'WINDOWS': False},
 'module': {'asyncio': <module 'asyncio' from '/data/data/com.termux/files/usr/lib/python3.11/asyncio/__init__.py'>,
            'colorama': <module 'colorama' from '/data/data/com.termux/files/usr/lib/python3.11/site-packages/colorama/__init__.py'>,
            'csv': <module 'csv' from '/data/data/com.termux/files/usr/lib/python3.11/csv.py'>,
            'datetime': <module 'datetime' from '/data/data/com.termux/files/usr/lib/python3.11/datetime.py'>,
            'functools': <module 'functools' from '/data/data/com.termux/files/usr/lib/python3.11/functools.py'>,
            'inspect': <module 'inspect' from '/data/data/com.termux/files/usr/lib/python3.11/inspect.py'>,
            'io': <module 'io' (frozen)>,
            'json': <module 'json' from '/data/data/com.termux/files/usr/lib/python3.11/json/__init__.py'>,
            'lxml': <module 'lxml' from '/data/data/com.termux/files/usr/lib/python3.11/site-packages/lxml/__init__.py'>,
            'math': <module 'math' from '/data/data/com.termux/files/usr/lib/python3.11/lib-dynload/math.cpython-311.so'>,
            'multiprocessing': <module 'multiprocessing' from '/data/data/com.termux/files/usr/lib/python3.11/multiprocessing/__init__.py'>,
            'operator': <module 'operator' from '/data/data/com.termux/files/usr/lib/python3.11/operator.py'>,
            'os': <module 'os' (frozen)>,
            'pathlib': <module 'pathlib' from '/data/data/com.termux/files/usr/lib/python3.11/pathlib.py'>,
            'pint': <module 'pint' from '/data/data/com.termux/files/usr/lib/python3.11/site-packages/pint/__init__.py'>,
            'pprint': <module 'pprint' from '/data/data/com.termux/files/usr/lib/python3.11/pprint.py'>,
            'queue': <module 'queue' from '/data/data/com.termux/files/usr/lib/python3.11/queue.py'>,
            'random': <module 'random' from '/data/data/com.termux/files/usr/lib/python3.11/random.py'>,
            're': <module 're' from '/data/data/com.termux/files/usr/lib/python3.11/re/__init__.py'>,
            'requests': <module 'requests' from '/data/data/com.termux/files/usr/lib/python3.11/site-packages/requests/__init__.py'>,
            'string': <module 'string' from '/data/data/com.termux/files/usr/lib/python3.11/string.py'>,
            'subprocess': <module 'subprocess' from '/data/data/com.termux/files/usr/lib/python3.11/subprocess.py'>,
            'sys': <module 'sys' (built-in)>,
            'textwrap': <module 'textwrap' from '/data/data/com.termux/files/usr/lib/python3.11/textwrap.py'>,
            'threading': <module 'threading' from '/data/data/com.termux/files/usr/lib/python3.11/threading.py'>,
            'time': <module 'time' (built-in)>,
            'tzdata': <module 'tzdata' from '/data/data/com.termux/files/usr/lib/python3.11/site-packages/tzdata/__init__.py'>,
            'uuid': <module 'uuid' from '/data/data/com.termux/files/usr/lib/python3.11/uuid.py'>,
            'webbrowser': <module 'webbrowser' from '/data/data/com.termux/files/usr/lib/python3.11/webbrowser.py'>,
            'yaml': <module 'yaml' from '/data/data/com.termux/files/usr/lib/python3.11/site-packages/yaml/__init__.py'>,
            'zoneinfo': <module 'zoneinfo' from '/data/data/com.termux/files/usr/lib/python3.11/zoneinfo/__init__.py'>}}
```

## log

`log(text=None)`

Decorator untuk mempermudah pembuatan log karena tidak perlu mengubah  
fungsi yg sudah ada.  
Melakukan print ke console untuk menginformasikan proses yg sedang  
berjalan didalam program.  
  
```py  
@log  
def some_function():  
    pass  
  
@log()  
def some_function_again():  
    pass  
  
@log("Calling some function")  
def some_function_more():  
    pass  
  
some_function()  
some_function_again()  
some_function_more()  
```

## oct_to_int

`oct_to_int(n)`

Fungsi ini berguna untuk mengubah angka octal   
menjadi angka integer.  
  
```python  
print(oct_to_int(oct(244)))  
```

Output:
```py
244
```

## password_generator

`password_generator(length=8, characters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')`

Membuat pssword secara acak  
  
```python  
print(password_generator())  
```

Output:
```py
Z[ElVvWE
```

## pip_freeze_without_version

`pip_freeze_without_version(filename=None)`

Memberikan list dari dependencies yang terinstall tanpa version.  
Bertujuan untuk menggunakan Batteries Included Python.  
  
```py  
print(pip_freeze_without_version())  
```

## poetry_publish

`poetry_publish(token=None)`

Publish project to pypi,org  
  
```py  
poetry_publish()  
```

## poetry_update_version

`poetry_update_version(mayor=False, minor=False, patch=False)`

Update versi pada pyproject.toml menggunakan poetry  
  
```py  
poetry_update_version()  
```

## print_dir

`print_dir(var, colorize=True)`

Print property dan method yang tersedia pada variabel  
  
```python  
import pathlib  
p = pathlib.Path("https://www.google.com/")  
print_dir(p, colorize=False)  
```

Output:
```py
           __bytes__ : b'https:/www.google.com'
           __class__ : .
             __dir__ : ['__module__', '__doc__', '__slots__', '__new__', '_make_child_relpath', '__enter__', '__exit__', 'cwd', 'home', 'samefile', 'iterdir', '_scandir', 'glob', 'rglob', 'absolute', 'resolve', 'stat', 'owner', 'group', 'open', 'read_bytes', 'read_text', 'write_bytes', 'write_text', 'readlink', 'touch', 'mkdir', 'chmod', 'lchmod', 'unlink', 'rmdir', 'lstat', 'rename', 'replace', 'symlink_to', 'hardlink_to', 'link_to', 'exists', 'is_dir', 'is_file', 'is_mount', 'is_symlink', 'is_block_device', 'is_char_device', 'is_fifo', 'is_socket', 'expanduser', '__reduce__', '_parse_args', '_from_parts', '_from_parsed_parts', '_format_parsed_parts', '_make_child', '__str__', '__fspath__', 'as_posix', '__bytes__', '__repr__', 'as_uri', '_cparts', '__eq__', '__hash__', '__lt__', '__le__', '__gt__', '__ge__', 'drive', 'root', 'anchor', 'name', 'suffix', 'suffixes', 'stem', 'with_name', 'with_stem', 'with_suffix', 'relative_to', 'is_relative_to', 'parts', 'joinpath', '__truediv__', '__rtruediv__', 'parent', 'parents', 'is_absolute', 'is_reserved', 'match', '_cached_cparts', '_drv', '_hash', '_parts', '_pparts', '_root', '_str', '__getattribute__', '__setattr__', '__delattr__', '__ne__', '__init__', '__reduce_ex__', '__getstate__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__', '_flavour']
             __doc__ : Path subclass for non-Windows systems.

    On a POSIX system, instantiating a Path should return this object.
    
           __enter__ : https:/www.google.com
          __fspath__ : https:/www.google.com
        __getstate__ : (None, {'_drv': '', '_root': '', '_parts': ['https:', 'www.google.com'], '_str': 'https:/www.google.com'})
            __hash__ : -6368168625464002048
            __init__ : None
   __init_subclass__ : None
          __module__ : pathlib
          __reduce__ : (<class 'pathlib.PosixPath'>, ('https:', 'www.google.com'))
            __repr__ : PosixPath('https:/www.google.com')
          __sizeof__ : 72
           __slots__ : ()
             __str__ : https:/www.google.com
    __subclasshook__ : NotImplemented
      _cached_cparts : ['https:', 'www.google.com']
             _cparts : ['https:', 'www.google.com']
                _drv : 
            _flavour : <pathlib._PosixFlavour object at 0x7a25714dd0>
               _hash : -6368168625464002048
              _parts : ['https:', 'www.google.com']
               _root : 
                _str : https:/www.google.com
            absolute : /data/data/com.termux/files/home/pypipr/https:/www.google.com
              anchor : 
            as_posix : https:/www.google.com
                 cwd : /data/data/com.termux/files/home/pypipr
               drive : 
              exists : False
          expanduser : https:/www.google.com
                home : /data/data/com.termux/files/home
         is_absolute : False
     is_block_device : False
      is_char_device : False
              is_dir : False
             is_fifo : False
             is_file : False
            is_mount : False
         is_reserved : False
           is_socket : False
          is_symlink : False
             iterdir : <generator object Path.iterdir at 0x7a10af2a40>
            joinpath : https:/www.google.com
                name : www.google.com
              parent : https:
             parents : <PosixPath.parents>
               parts : ('https:', 'www.google.com')
             resolve : /data/data/com.termux/files/home/pypipr/https:/www.google.com
                root : 
                stem : www.google
              suffix : .com
            suffixes : ['.google', '.com']
```

## print_to_last_line

`print_to_last_line(text: str, latest=1, clear=True)`

Melakukan print ke konsol tetapi akan menimpa baris terakhir.  
Berguna untuk memberikan progress secara interaktif.  
  
```py  
c = input("masukkan apa saja : ")  
print_to_last_line(f"masukkan apa saja : {c} [ok]")  
```

## random_bool

`random_bool()`

Menghasilkan nilai random True atau False.  
Fungsi ini merupakan fungsi tercepat untuk mendapatkan random bool.  
Fungsi ini sangat cepat, tetapi pemanggilan fungsi ini membutuhkan  
overhead yg besar.  
  
```python  
print(random_bool())  
```

Output:
```py
True
```

## restart

`restart(*argv)`

Mengulang program dari awal seperti memulai awal.  
  
Bisa ditambahkan dengan argumen tambahan  
  
```py  
restart("--stdio")  
```

## set_timeout

`set_timeout(interval, func, args=None, kwargs=None)`

Menjalankan fungsi ketika sudah sekian detik.  
Apabila timeout masih berjalan tapi kode sudah selesai dieksekusi semua, maka  
program tidak akan berhenti sampai timeout selesai, kemudian fungsi dijalankan,  
kemudian program dihentikan.  
  
```python  
set_timeout(3, lambda: print("Timeout 3"))  
x = set_timeout(7, print, args=["Timeout 7"])  
print(x)  
print("menghentikan timeout 7")  
x.cancel()  
```

Output:
```py
<Timer(Thread-2, started 524237651184)>
menghentikan timeout 7
```

## sets_ordered

`sets_ordered(iterator)`

Hanya mengambil nilai unik dari suatu list  
  
```python  
array = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]  
print(sets_ordered(array))  
print(list(sets_ordered(array)))  
```

Output:
```py
<generator object sets_ordered at 0x7a10b24fb0>
[2, 3, 12, 42, 1, 43, 41, 4, 24, 32]
```

## str_cmp

`str_cmp(t1, t2)`

Membandingakan string secara incase-sensitive menggunakan lower().  
Lebih cepat dibandingkan upper(), casefold(), re.fullmatch(), len().  
perbandingan ini sangat cepat, tetapi pemanggilan fungsi ini membutuhkan  
overhead yg besar.  
  
```python  
print(str_cmp('teks1', 'Teks1'))  
```

Output:
```py
True
```

## text_colorize

`text_colorize(text, color='\x1b[32m', bright='\x1b[1m', color_end='\x1b[0m')`

return text dengan warna untuk menunjukan text penting  
  
```py  
text_colorize("Print some text")  
text_colorize("Print some text", color=colorama.Fore.RED)  
```

# CLASS

## APIMixinView

`APIMixinView()`

APIView adalah class view untuk membuat Website API  
  
Cara kerjanya adalah dengan menggunakan variabel GET  
untuk menerima data.  
Cara ini dipilih untuk menghindari CORS protection.  
  
Key dan value dari parameter get akan disimpan  
dalam variabel dictionary APIDict yg bisa langsung  
diakses.  
  
Class ini tidak bisa digunakan sendiri.  
Class ini harus menjadi mixin Class View karena  
perlu trigger untuk memanggil method get().  
  
  
```py  
class ExampleTodoAddView(APIMixinView, View):  
    def process_data(self, *args, **kwargs):  
        return TodoModel.objects.create(**self.APIDict)  
```

## ComparePerformance

`ComparePerformance()`

Menjalankan seluruh method dalam class,  
Kemudian membandingkan waktu yg diperlukan.  
Nilai 100 berarti yang tercepat.  
  
```python  
class ExampleComparePerformance(ComparePerformance):  
    # number = 1  
    z = 10  
  
    def a(self):  
        return (x for x in range(self.z))  
  
    def b(self):  
        return tuple(x for x in range(self.z))  
  
    def c(self):  
        return [x for x in range(self.z)]  
  
    def d(self):  
        return list(x for x in range(self.z))  
  
pprint.pprint(ExampleComparePerformance().compare_result(), depth=100)  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
```

Output:
```py
{'a': <generator object ExampleComparePerformance.a.<locals>.<genexpr> at 0x7a10b24ad0>,
 'b': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
 'c': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
 'd': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}
{'a': 130, 'b': 132, 'c': 100, 'd': 191}
{'a': 107, 'b': 141, 'c': 100, 'd': 198}
{'a': 107, 'b': 131, 'c': 100, 'd': 163}
{'a': 109, 'b': 124, 'c': 100, 'd': 151}
{'a': 105, 'b': 130, 'c': 100, 'd': 153}
```

## PintUregQuantity

`PintUregQuantity(value, units=None)`

## RunParallel

`RunParallel()`

Menjalankan program secara bersamaan.  
  
- `class RunParallel` didesain hanya untuk pemrosesan data saja.  
- Penggunaannya `class RunParallel` dengan cara membuat instance  
  sub class beserta data yg akan diproses, kemudian panggil fungsi  
  yg dipilih `run_asyncio / run_multi_threading / run_multi_processing`,  
  kemudian dapatkan hasilnya.  
- `class RunParallel` tidak didesain untuk menyimpan data, karena  
  setiap module terutama module `multiprocessing` tidak dapat mengakses  
  data kelas dari proses yg berbeda.  
- Semua methods akan dijalankan secara paralel kecuali method dengan  
  nama yg diawali underscore `_`  
- Method untuk multithreading/multiprocessing harus memiliki 2  
  parameter, yaitu: `result: dict` dan `q: queue.Queue`. Parameter  
  `result` digunakan untuk memberikan return value dari method, dan  
  Parameter `q` digunakan untuk mengirim data antar proses.  
- Method untuk asyncio harus menggunakan keyword `async def`, dan  
  untuk perpindahan antar kode menggunakan `await asyncio.sleep(0)`,  
  dan keyword `return` untuk memberikan return value.  
- Return Value berupa dictionary dengan key adalah nama function,  
  dan value adalah return value dari setiap fungsi  
- Menjalankan Multiprocessing harus berada dalam blok  
  `if __name__ == "__main__":` karena area global pada program akan  
  diproses lagi. Terutama pada sistem operasi windows.  
- `run_asyncio()` akan menjalankan kode dalam satu program, hanya  
  saja alur program dapat berpindah-pindah menggunkan  
  `await asyncio.sleep(0)`.  
- `run_multi_threading()` akan menjalankan program dalam satu CPU,  
  hanya saja dalam thread yang berbeda. Walaupun tidak benar-benar  
  berjalan secara bersamaan namun bisa meningkatkan kecepatan  
  penyelesaian program, dan dapat saling mengakses resource antar  
  program.  Akses resource antar program bisa secara langsung maupun  
  menggunakan parameter yang sudah disediakan yaitu `result: dict`  
  dan `q: queue.Queue`.  
- `run_multi_processing()` akan menjalankan program dengan beberapa  
  CPU. Program akan dibuatkan environment sendiri yang terpisah dari  
  program induk. Keuntungannya adalah program dapat benar-benar berjalan  
  bersamaan, namun tidak dapat saling mengakses resource secara langsung.  
  Akses resource menggunakan parameter yang sudah disediakan yaitu  
  `result: dict` dan `q: queue.Queue`.  
  
```py  
class ExampleRunParallel(RunParallel):  
    z = "ini"  
  
    def __init__(self) -> None:  
        self.pop = random.randint(0, 100)  
  
    def _set_property_here(self, v):  
        self.prop = v  
  
    def a(self, result: dict, q: queue.Queue):  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["a"] = "a"  
        q.put("from a 1")  
        q.put("from a 2")  
  
    def b(self, result: dict, q: queue.Queue):  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["b"] = "b"  
        result["q_get"] = q.get()  
  
    def c(self, result: dict, q: queue.Queue):  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["c"] = "c"  
        result["q_get"] = q.get()  
  
    async def d(self):  
        print("hello")  
        await asyncio.sleep(0)  
        print("hello")  
  
        result = {}  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["d"] = "d"  
        return result  
  
    async def e(self):  
        print("world")  
        await asyncio.sleep(0)  
        print("world")  
  
        result = {}  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["e"] = "e"  
        return result  
  
if __name__ == "__main__":  
    print(ExampleRunParallel().run_asyncio())  
    print(ExampleRunParallel().run_multi_threading())  
    print(ExampleRunParallel().run_multi_processing())  
```
