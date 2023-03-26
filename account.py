# -*- coding: utf-8 -*-
""" account.py -- Leitor de Extractos do cartao Universo

(c)2023  Henrique Moreira
"""

class MovCard():
    """ Card movements """
    _invalid_default = "?"

    def __init__(self, acc_number:str, country_abbrev:str="us"):
        self._value = acc_number.replace(" ", "").replace(".", "")
        self._valid = self._value.isalnum()
        self._country = country_abbrev

    def valid(self) -> bool:
        """ Returns 'True' if is valid """
        return self._valid

    def string(self) -> str:
        assert self._value
        return self._value

    def __str__(self):
        if not self._value:
            return MovCard._invalid_default
        return self._value

class Movements(MovCard):
    def __init__(self, value:str=""):
        super().__init__(value, "pt")
        _, self._valid, _ = self._validate_number(self._value)

    def _validate_number(self, acc_number:str) -> tuple:
        """ Returns ('UV', whether_account_number_is_valid, last_four_digits """
        assert isinstance(acc_number, str)
        kind = "UV"
        ref = acc_number[:-4]
        is_valid = self._valid
        return (kind, is_valid, ref)
