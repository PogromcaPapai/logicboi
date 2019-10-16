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


def strip(_list, value_dict): #TODO: Nie działa kompletnie; zrobić tak, aby komputer najpierw poszukiwał spójników?
    ''' Converts a `list` into a data tree '''
    brackets = 0
    for i in range(len(_list)):
        for j in _list[i]:
            if j=='(':
                brackets += 1
            elif j==')':
                brackets -= 1
        name = _list[i][:]
        name = name.replace('(', '').replace(')', '') #Bracket deletion
        if name in SYNTAX_DICT.keys() and brackets in [0, 1]:
            arg_amount = SYNTAX_DICT[name]('', None, None, None).arg_number
            if arg_amount == 1:
                part1 = strip(_list[i:], value_dict)
                return SYNTAX_DICT[name]('', None, part1)
            elif arg_amount == 2:
                part1 = strip(_list[i:], value_dict)
                part2 = strip(_list[:i], value_dict)
                return SYNTAX_DICT[name]('', None, part1, part2)
            else:
                raise Exception('This version doesn\'t support this amount of arguments')
        elif name in value_dict.keys():
            return Sentence(name, value_dict[name])

############### __main__ ###############
if __name__ == "__main__":
    _dict = {'p':True,'q':False}
    zdanie = '(p and q)'
    wynik = strip(zdanie.split(), _dict)
    print(wynik.evaluate())
