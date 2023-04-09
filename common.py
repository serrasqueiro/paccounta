# -*- coding: utf-8 -*-
""" common.py -- part of 'paccounta'

(c)2023  Henrique Moreira
"""

import unidecode

EURO_ASCII128 = '\x80'	# Windows-1252 (ASCII 128d = 0x80)


class Textual():
    """ General textual abstract clas """
    _invalid_char = "?"
    _eur_as_dollar = "$"

    def __init__(self, preferred="us"):
        self._preferred = preferred

    def preferred(self) -> bool:
        """ Returns the preferred two-letter country code """
        if self._preferred:
            return self._preferred
        return "us"

class Ascii(Textual):
    def __init__(self, obj=None, preferred=""):
        super().__init__(preferred)
        self._obj = "" if obj is None else obj

    def getter(self):
        return self._obj

    def string(self, astr):
        assert isinstance(astr, str)
        return Ascii.simple(astr)

    @staticmethod
    def simple(astr):
        assert isinstance(astr, str)
        as_dollar = Textual._eur_as_dollar
        if as_dollar:
            astr = astr.replace(EURO_ASCII128, as_dollar)
            astr = astr.replace(chr(0x20AC), as_dollar)
        return unidecode.unidecode(astr)
