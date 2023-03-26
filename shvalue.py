# -*- coding: utf-8 -*-
""" shvalue.py -- Leitor de Extractos do cartao Universo

(c)2023  Henrique Moreira
"""

class Value():
    """ Value """
    def __init__(self, cell):
        self._dtype = "s"  # default is 's'=string
        if cell is None:
            what = "-"
        elif isinstance(cell, (str, int)):
            what = cell
        else:
            what = cell.value
            self._dtype = cell.data_type
        self._value = "-" if what is None else what

    def string(self) -> str:
        aval = self._value
        if self._dtype == "s":
            astr = aval
        elif self._dtype == "n":
            astr = f"{aval}"
        else:
            astr = aval
            assert isinstance(astr, str), self._dtype
        return astr

    def data_type(self):
        return self._dtype

    def __str__(self):
        return self.string()

    def __eq__(self, new):
        return self._value == new

    def __ne__(self, new):
        return self._value == new

    def __repr__(self):
        return self.string()
