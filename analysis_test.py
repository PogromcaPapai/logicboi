import logicboi
import pytest

class TestTXT:
    def test_all(self):
        with open('formulas to test.txt', "r") as text:
            while True:
                line = text.readline()
                if line=="":
                    break
                sent, val = line.split(";")
                val = bool(int(val))
                sent_split = sent.split()
                calculated = True
                for _dict in [{'p':False,'q':True}, {'p':True,'q':True}, {'p':False,'q':False}, {'p':True,'q':False}]:
                    zdanienew = logicboi.into_prefix(logicboi.syntax_analysis(sent_split), _dict)
                    wynik = logicboi.parse(zdanienew, _dict)
                    calculated &= wynik.evaluate()
                assert calculated == val