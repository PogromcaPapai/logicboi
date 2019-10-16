from functools import reduce

class Sentence(object):
    truth_table = dict()
    arg_number = 0

    def __init__(self, string, value, *args):
        '''
        Creates a representation of a sentence

        Args:
         - `string` - `string` - used as a character representation of the sentence, ex. `p, q, p^q`  
         - `value` - `True/False/None` - used to provide an input for sentence's logical value (None if unknown)  
         - `*args` - `Sentence` - used to input arguments of the sentence
        '''
        super().__init__()
        self.string = string
        self.value = value
        if not self.arg_number == len(args):
            raise TypeError("This amount of arguments is not allowed here: {0}".format(self.__str__()))
        self.args = args

    def __repr__(self):
        return "{0} [{1}]".format(self.string, self.value)

    def __str__(self):
        return self.string

    def evaluate(self):
        ''' Evaluates the value of the sentence '''
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

Verum = Sentence("T", True)
Falsum = Sentence("F", False)

class Negation(Sentence):
    truth_table = {True:False, False:True}
    arg_number = 1

class Conjunction(Sentence):
    truth_table = {True:{True:True, False:False}, False:{True:False, False:False}}
    arg_number = 2

class Alternative(Sentence):
    truth_table = {True:{True:True, False:True}, False:{True:True, False:False}}
    arg_number = 2

class Implication(Sentence):
    truth_table = {True:{False:False, True:True}, False:{False:True, True:True}}
    arg_number = 2

if __name__ == "__main__":
    test1 = Sentence('', True)
    test2 = Sentence('', True)
    tested = Conjunction('', None, test1, test2)
    print(tested.evaluate())