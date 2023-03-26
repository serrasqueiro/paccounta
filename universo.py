# -*- coding: utf-8 -*-
""" universo.py -- Leitor de Extractos do cartao Universo

(c)2023  Henrique Moreira
"""

import datetime
import openpyxl
from paccounta.shvalue import Value

def main():
    fname = "../../repo/universopt/_extractos/UNIVERSO_Movimentos_20230326_111102.xlsx"
    read_test(fname)

def dump_line(line, idx=0):
    assert idx >= 0
    data, desc, cname, when, aval, desconto, what = line
    slug = ",".join(better_date(data).split(" "))
    astr = f"{slug},{cname},@{what},{desc},{when},{euro_value(aval)}"
    print(astr)

def read_test(in_xcel:str, verbose=0):
    filename = in_xcel
    data = openpyxl.open(filename, read_only=True)
    assert data.sheetnames == ['UNIVERSO_Movimentos']
    sht = data[data.sheetnames[0]]
    mov = Movimentos(sht, filename)
    for one in mov.sequence():
        idx, line = one[0], one[1:]
        if verbose > 0:
            print(idx, line)
        else:
            dump_line(line, idx)
    return mov

class Reader():
    """ Generic readout """
    def __init__(self, fname=""):
        self._fname = fname

class Movimentos(Reader):
    """ Movements of 'Universo' """
    def __init__(self, sht, fname=""):
        super().__init__(fname)
        self.there, self._seq = self._skel(sht)
        assert self.there, sht.title

    def sequence(self):
        return self._seq

    def _skel(self, sht):
        """ Parses Excel rows
		Data	Movimento	Cartão	Modalidade	Montante	Descontos	Categoria
	1. data dd-mm-yyy
	2. descricao do movimento
	3. nome que consta no cartao, ou cartao virtual
	4. modalidade: fim do mes (FDM)
	5. descontos ('A calcular', ...ou valor)
	6. categoria atribuida:
		a Alimentacao
		b Casa
		c Entertenimento
		d Outros
		e Restauracao
		f Saude e Bem Estar
		g Transportes
		h Vestuario
		i Viagens
		z em branco (não aplicável)
        """
        assert isinstance(sht.title, str)
        assert len(sht.title) > 8, sht.title
        there = [[idx] + row_string(row) for idx, row in enumerate(sht, 1)]
        prefix = [[0] + [chr(ord('A') + idx) for idx in range(len(there[-1]))]]
        there = prefix + there
        head = there[2]
        assert head[1] == "Data", head
        alist = there[2 + int(head[1] == "Data"):][::-1]
        return there, alist

def row_string(row):
    res = []
    for idx, aval in enumerate(row):
        col = chr(ord('A') + idx)
        new = Value(aval)
        elem = new.string()
        if col == "A":
            item = dttm_from_date(new)
        elif col == "B":
            item = better_description(elem)
        elif col == "C":
            item = shorter_card_name(elem)
        elif col == "D":
            if elem.upper().startswith("FIM"):
                item = "FDM"
            else:
                item = elem
        elif col == "E":
            if elem.lower() in ("-", "montante"):
                item = ""
            else:
                item = float(elem)
        elif col == "G" and elem.lower() != "categoria":
            item = lettering_kind(elem)
        else:
            item = [new]
        res.append(item)
    return res

def dttm_from_date(astr):
    fmt = "%d-%m-%Y"
    #try:
    #    dttm =  datetime.datetime.strptime(astr, fmt)
    #except TypeError:
    #    dttm = astr
    data = astr.string()
    if data.count("-") == 2:
        dttm =  datetime.datetime.strptime(data, fmt)
        return dttm
    return data

def better_date(dttm) -> str:
    out_fmt = "%Y-%d-%m %a"
    new = dttm.strftime(out_fmt)
    return new

def lettering_kind(astr):
    """ Returns one letter classifier from string. """
    if not astr or astr == '-':
        return 'z'
    astr = astr.lower()
    astr = astr.replace(chr(250), "u")
    match = {
        "alim": 'a',
        "casa": 'b',
        "entretenimento": 'c',
        "outros": 'd',
        "rest": 'e',
        "saud": 'f',
        "transportes": 'g',
        "vest": 'h',
        "viag": 'i',
    }
    what = match.get(astr[:4])
    if what is not None:
        return what
    what = match.get(astr)
    assert what is not None, astr
    return what

def shorter_card_name(astr):
    spl = astr.split(" ")
    astr = ""
    for part in spl:
        if astr:
            astr += "_"
        astr += part[:3]
    if astr == "-":
        res = "-" * 7
    else:
        res = f"{astr:.<7}"
    return res

def euro_value(aval):
    assert isinstance(aval, float), f"Bogus money: {aval}"
    return f"{aval:.2f}"

def better_description(astr, achr=' '):
    def slim_str(new):
        return new.replace("*", "")
    lin = achr.join([slim_str(aba) for aba in astr.split(" ") if aba])
    lin = lin.replace(",", ";")
    return lin

if __name__ == '__main__':
    main()
