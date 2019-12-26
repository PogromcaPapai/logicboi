import logicboi.tree as logicboi
import pytest

def basetest(model_class, tested_function, *values):
    sentences = []
    for i in values:
        sentences.append(logicboi.Sentence(str(i), i))
    correct_val = tested_function(*values)
    tested = model_class('', None, *sentences)
    assert tested.evaluate() == correct_val
    

class TestNegation:

    def test_true(self):
        basetest(logicboi.Negation, lambda x: not x, True)

    def test_false(self):
        basetest(logicboi.Negation, lambda x: not x, False)

    def test_additional(self):
        with pytest.raises(TypeError):
            logicboi.Negation('', None, logicboi.Sentence('', None), logicboi.Sentence('', None))

class TestConjunction:

    def test_truextrue(self):
        basetest(logicboi.Conjunction, lambda x,y: x and y, True, True)

    def test_falsextrue(self):
        basetest(logicboi.Conjunction, lambda x,y: x and y, False, True)

    def test_truexfalse(self):
        basetest(logicboi.Conjunction, lambda x,y: x and y, True, False)

    def test_falsexfalse(self):
        basetest(logicboi.Conjunction, lambda x,y: x and y, False, False)

    def test_additional(self):
        with pytest.raises(TypeError):
            logicboi.Conjunction('', None, logicboi.Sentence('', None), logicboi.Sentence('', None), logicboi.Sentence('', None))

class TestAlternative:

    def test_truextrue(self):
        basetest(logicboi.Alternative, lambda x,y: x or y, True, True)

    def test_falsextrue(self):
        basetest(logicboi.Alternative, lambda x,y: x or y, False, True)

    def test_truexfalse(self):
        basetest(logicboi.Alternative, lambda x,y: x or y, True, False)

    def test_falsexfalse(self):
        basetest(logicboi.Alternative, lambda x,y: x or y, False, False)

    def test_additional(self):
        with pytest.raises(TypeError):
            logicboi.Alternative('', None, logicboi.Sentence('', None), logicboi.Sentence('', None), logicboi.Sentence('', None))

class TestImplication:

    def test_truextrue(self):
        basetest(logicboi.Implication, lambda x,y: (not x) or y, True, True)

    def test_falsextrue(self):
        basetest(logicboi.Implication, lambda x,y: (not x) or y, False, True)

    def test_truexfalse(self):
        basetest(logicboi.Implication, lambda x,y: (not x) or y, True, False)

    def test_falsexfalse(self):
        basetest(logicboi.Implication, lambda x,y: (not x) or y, False, False)

    def test_additional(self):
        with pytest.raises(TypeError):
            logicboi.Implication('', None, logicboi.Sentence('', None), logicboi.Sentence('', None), logicboi.Sentence('', None))