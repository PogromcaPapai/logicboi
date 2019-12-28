from copy import deepcopy
from functools import reduce

#### Back-End ####

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
        new_args = self.clean_args(args)
        if not self.arg_number == len(new_args):
            raise TypeError(
                "This amount of arguments is not allowed here")
        self.args = new_args

    def __repr__(self):
        return "{0} [{1}]".format(self.string, self.value)

    def __str__(self):
        return self.string

    @staticmethod
    def clean_args(args):
        new = []
        for i in args:
            if i!=None:
                new.append(i)
        return new

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

def gen_values(variables):
    var_list = list(variables)
    if len(var_list)==0:
        return [dict()]
    rec = gen_values(var_list[1:])
    trued = deepcopy(rec)
    falsed = deepcopy(rec)
    for i in trued:
        i[var_list[0]]=True
    for i in falsed:
        i[var_list[0]]=False
    new = trued + falsed
    return new

###
# Functor definitions
###

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


TREE_DICT = {'and': Conjunction, 'or': Alternative, 'not': Negation, 'imp': Implication}

#### Front-End ####

def parse(sentence, var_dict):
    ''' Parses `sentence` into a tree`; `sentence` needs to be in prefix notation'''
    def _recurparse(sentence, var_dict):
        symbol = TREE_DICT.get(sentence[0], Sentence)
        args = []
        new_sentence = sentence[1:]
        name = " ".join(sentence)
        for i in range(symbol.arg_number):
            arg, new_sentence = _recurparse(new_sentence, var_dict)
            args.append(arg)
        return symbol(name, var_dict.get(sentence[0], None), *args), new_sentence
    
    return _recurparse(sentence, var_dict)[0]
