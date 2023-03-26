""" nif.py -- module for portuguese NIF (taxpayer identification number -- TIN)

(c)2023  Henrique Moreira (obsoletes 'paccount.ptaccount')
"""

class TIN():
    """ Taxpayer Identification number """
    _invalid_default = "?"

    def __init__(self, value:str, country_abbrev:str="us"):
        self._valid = False
        self._value = value.replace(" ", "").replace(".", "")
        self._c_abbrev = country_abbrev

    def valid(self) -> bool:
        """ Returns 'True' if is valid """
        return self._valid

    def string(self) -> str:
        assert self._value
        return self._value

    def __str__(self):
        if not self._value:
            return TIN._invalid_default
        return self._value

class NIF(TIN):
    def __init__(self, value:str=""):
        super().__init__(value, "pt")
        _, self._valid, _ = self.pt_nif_valid(self._value)

    def pt_nif_valid(self, str_nif:str):
        """ Returns the tuple ("valid NIF", isOk?, check_digit)
        """
        err_result = ("", False, -1)
        assert isinstance(str_nif, str)
        if len(str_nif) != 9:
            return err_result
        first_allow = "125689"
        achr = str_nif[ 0 ]
        idx = first_allow.find(achr)
        if idx < 0:
            return err_result
        check_digit = 0
        idx = 1
        while idx < 9:
            a_val = ord(str_nif[ idx-1 ]) - ord('0')
            if a_val < 0 or a_val > 9:
                return err_result
            check_digit += (a_val * (10-idx))
            idx += 1
        f_digit = check_digit % 11
        if f_digit in (0, 1):
            f_digit = 0
        else:
            f_digit = 11 - f_digit
        idx -= 1
        a_val = ord(str_nif[idx]) - ord('0')
        if a_val == f_digit:
            return (str_nif, True, f_digit)
        corrected = str_nif[:idx] + chr(ord('0') + f_digit)
        return (corrected, False, f_digit)

    def what_valid(self):
        corrected, _, f_digit = self.pt_nif_valid(self._value)
        assert f_digit >= 0, self._value
        return corrected

# Hints
#	new = NIF("500 883 823")	# Please donate to UNICEF
#	print(new, "; valid()", new.valid(), end=f" << NIF('{new.string()}')\n")
#	print(NIF("500 883 82" + "4").what_valid(), "; corrected bogus check-digit")
