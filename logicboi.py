from functools import reduce
import re
from sys import argv as command
import logging

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
        new_args = self.clear_args(args)
        if not self.arg_number == len(new_args):
            raise TypeError(
                "This amount of arguments is not allowed here")
        self.args = new_args

    def __repr__(self):
        return "{0} [{1}]".format(self.string, self.value)

    def __str__(self):
        return self.string

    @staticmethod
    def clear_args(args):
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

############### Low-Level Front End ###############

SYNTAX_DICT = {'oraz':'and', '&':'and', 
               'lub':'or', '+':'or', 
               '~':'not', 
               '->':'imp', '>':'imp'}

def cut(sentence, val):
    ### RIGHT ###
    right = sentence[val+1:]
    right[0] = right[0].replace("(","", 1)
    right[-1] = right[-1].replace(")","", 1)
    ### LEFT  ###
    left = sentence[:val]
    if val>0:
        left[0] = left[0].replace("(","", 1)
        left[-1] = left[-1].replace(")","", 1)
    return left, right

def strip_options(command):
    option_pattern = re.compile(r'^[-]{2}.+')
    main_command, sentence = command
    options = []
    for word in sentence[:]:
        if option_pattern.match(word):
            sentence.pop(word)
            options.append(word)
    return main_command, options, sentence

def syntax_analysis(sentence):
    new = []
    for i in sentence:
        for j in SYNTAX_DICT.keys():
            i = i.replace(j, SYNTAX_DICT[j])
        new.append(i)
    return new

def into_prefix(sentence, value_list, infix_functors = ['and','or','imp'], prefix_functors = ['not']):
    ''' Converts the sentence (list of words) into a prefix notation '''
    brackets = 0
    for i in range(len(sentence)):
            brackets += sentence[i].count("(")
            brackets -= sentence[i].count(")")
            assert brackets >= 0, "Brackets not opened"
            if sentence[i] in infix_functors and brackets==0:
                new = cut(sentence, i)
                right = into_prefix(new[1], value_list, infix_functors = infix_functors)
                left = into_prefix(new[0], value_list, infix_functors = infix_functors)
                return [sentence[i]]+left+right
            elif sentence[i] in prefix_functors and brackets==0:
                new = cut(sentence, 0)
                right = into_prefix(new[1], value_list, prefix_functors = prefix_functors)
                return [sentence[i]]+right
    return sentence

def _recurparse(sentence, var_dict):
    ''' 
        USE `parse` INSTEAD OF THIS'''
    symbol = TREE_DICT.get(sentence[0], Sentence)
    args = []
    new_sentence = sentence[1:]
    name = " ".join(sentence)
    for i in range(symbol.arg_number):
        arg, new_sentence = _recurparse(new_sentence, var_dict)
        args.append(arg)
    return symbol(name, var_dict.get(sentence[0], None), *args), new_sentence

def parse(sentence, var_dict):
    return _recurparse(sentence, var_dict)[0]

############### __main__ ###############
if __name__ == "__main__":
    for _dict in [{'p':False,'q':True}, {'p':True,'q':True}, {'p':False,'q':False}, {'p':True,'q':False}]:
        zdanie = '(not (p or q)) -> ((not p) and (not q))'
        zdanie = into_prefix(syntax_analysis(zdanie.split()), _dict)
        wynik = parse(zdanie, _dict)
        print(wynik.evaluate())
