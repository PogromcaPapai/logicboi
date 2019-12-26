import logicboi.tree as tree
from logicboi.__main__ import into_prefix, syntax_analysis
import pytest

class TestTXT:
    def test_all(self):
        with open('tests/formulas to test.txt', "r") as text:
            while True:
                line = text.readline()
                if line=="":
                    break
                sent, val = line.split(";")
                val = bool(int(val))
                sent_split = sent.split()
                calculated = True
                for _dict in [{'p':False,'q':True}, {'p':True,'q':True}, {'p':False,'q':False}, {'p':True,'q':False}]:
                    zdanienew = into_prefix(syntax_analysis(sent_split), _dict)
                    wynik = tree.parse(zdanienew, _dict)
                    calculated &= wynik.evaluate()
                assert calculated == val