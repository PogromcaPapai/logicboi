from functools import reduce

class Sentence(object):
    truth_table = dict()
    arg_number = 0

    def __init__(self, args, string='', value=None):
        super().__init__()
        self.string = string
        self.value = value
        assert self.arg_number == len(args), "This amount of arguments is not allowed here: {0}".format(self.__str__())
        self.args = args

    def __repr__(self):
        return "{0} [{1}]".format(self.string, self.value)

    def __str__(self):
        return self.string

    def evaluate(self):
        if self.value != None:
            pass
        elif self.truth_table == None:
            raise Exception("Sentence not defined")
        else:
            self.value = reduce(lambda x, y: x[y.evaluate()], self.args, self.truth_table)
        return self.value

######
### Functor definitions 
######

Verum = Sentence([], string="T", value=True)
Falsum = Sentence([], string="F", value=False)

class Negation(Sentence):
    truth_table = {True:False, False:True}
    arg_number = 1

class Conjunction(Sentence):
    truth_table = {True:{True:True, False:False}, False:{True:False, False:False}}
    arg_number = 2

class Alternative(Sentence):
    truth_table = {True:{True:True, False:True}, False:{True:True, False:False}}
    arg_number = 2

if __name__ == "__main__":
    test1 = Sentence([], value=True)
    test2 = Sentence([], value=True)
    tested = Conjunction([test1, test2])
    print(tested.evaluate())