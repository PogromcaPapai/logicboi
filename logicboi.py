from functools import reduce
import re
from sys import argv as command

############### Back End ###############


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
            raise TypeError(
                "This amount of arguments is not allowed here: {0}".format(self.__str__()))
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
            self.value = reduce(
                lambda x, y: x[y.evaluate()], self.args, self.truth_table)
        return self.value

###
# Functor definitions
###


Verum = Sentence("T", True)
Falsum = Sentence("F", False)


class Negation(Sentence):
    truth_table = {True: False, False: True}
    arg_number = 1


class Conjunction(Sentence):
    truth_table = {True: {True: True, False: False},
                   False: {True: False, False: False}}
    arg_number = 2


class Alternative(Sentence):
    truth_table = {True: {True: True, False: True},
                   False: {True: True, False: False}}
    arg_number = 2


class Implication(Sentence):
    truth_table = {True: {False: False, True: True},
                   False: {False: True, True: True}}
    arg_number = 2


SYNTAX_DICT = {'and': Conjunction, 'i': Conjunction, '&': Conjunction, 'or': Alternative,
               'lub': Alternative, '+': Alternative, '~': Negation, 'not': Negation, 'imp': Implication, ">": Implication}

############### Front End ###############


def strip_options(_list):
    option_pattern = re.compile(r'^[-]{2}.+')
    main_command, sentence = _list
    options = []
    for word in sentence[:]:
        if option_pattern.match(word):
            sentence.pop(word)
            options.append(word)
    return main_command, options, sentence


def strip(_list, value_dict):
    ''' Converts a `list` into a data tree '''
    brackets = 0
    for i in range(_list):
        for j in _list[i]:
            if j=='(':
                brackets += 1
            elif j==')':
                brackets -= 1
        i_clone = _list[i][:]
        i_clone.replace('(', ''); i_clone.replace(')', '') #Bracket deletion
        if i_clone in SYNTAX_DICT.keys() and brackets == 1:
            arg_amount = SYNTAX_DICT[i_clone]('', None).arg_number
            if arg_amount == 1:
                part1 = strip(_list[i+1:], value_dict)
                return SYNTAX_DICT[i_clone]('', None, part1)
            elif arg_amount == 2:
                part1 = strip(_list[i+1:], value_dict)
                part2 = strip(_list[:i-1], value_dict)
                return SYNTAX_DICT[i_clone]('', None, part1, part2)
            else:
                raise Exception('This version doesn\'t support this amount of arguments')
        elif i_clone in value_dict.keys():
            return Sentence(i_clone, value_dict[i_clone])

############### __main__ ###############
if __name__ == "__main__":
    pass
