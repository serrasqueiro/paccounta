# -*- coding: utf-8 -*-
""" uvextract.py -- text reader

(c)2023  Henrique Moreira
"""

import datetime
import openpyxl
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
    res = Ascii().simple(astr)
    return res
