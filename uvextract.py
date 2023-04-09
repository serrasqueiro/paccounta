# -*- coding: utf-8 -*-
""" uvextract.py -- text reader

(c)2023  Henrique Moreira
"""

from paccounta.common import Ascii

IN_ENCODING = "utf-8"

def main():
    fname = "extractos/extracto.txt"
    read_test(fname)

def read_test(fname:str, verbose=0):
    lines = reader_text_movements(fname)
    if verbose > 0:
        print(lines)
    return lines

def reader_text_movements(fname:str) -> list:
    with open(fname, "r", encoding=IN_ENCODING) as fdin:
        lines = [linear_line(line.strip(), idx) for idx, line in enumerate(fdin.readlines(), 1) if line.strip()]
    return lines

def linear_line(astr:str, idx=0):
    here = Ascii().simple(astr)
    res = here.replace(" $", "$")
    return res

def mov1_pattern():
    """ Extracto, linha com movimento
	14/03 15/03 Compra Pay Portugal 0,00$ -81,41$ 0,81$ 1,00%

	Stored:	https://regex101.com/r/6kkUwx/1
	Delete this regex: https://regex101.com/delete/1em6P5vJMNcshJjVWmSi6EURJRuv46Uz395y
    """
    pat = r"(\d*[\/]\d*) (\d*[\/]\d*)(.*) ([-]?\d\d*,\d*[$]) ([-]?\d\d*,\d*[$])[ ]+(\d,\d*[%]?)$"
    pattern = re.compile(pat)
    return pattern
