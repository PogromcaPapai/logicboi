import logicboi
import pytest


class TestNegation:

    def test_true(self):
        test = logicboi.Sentence([], value=True)
        tested = logicboi.Negation([test])
        assert tested.evaluate() == False

    def test_false(self):
        test = logicboi.Sentence([], value=False)
        tested = logicboi.Negation([test])
        assert tested.evaluate() == True

    def test_additional(self):
        with pytest.raises(AssertionError):
            logicboi.Negation([logicboi.Sentence([]), logicboi.Sentence([])])

class TestConjunction:

    def test_truextrue(self):
        test1 = logicboi.Sentence([], value=True)
        test2 = logicboi.Sentence([], value=True)
        tested = logicboi.Conjunction([test1, test2])
        assert tested.evaluate() == True

    def test_additional(self):
        with pytest.raises(AssertionError):
            logicboi.Negation([logicboi.Sentence([]), logicboi.Sentence([]), logicboi.Sentence([])])