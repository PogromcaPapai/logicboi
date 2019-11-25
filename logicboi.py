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
        if not self.arg_number == len(args):
            raise TypeError(
                "This amount of arguments is not allowed here")
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

############### Front End ###############

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
    left[0] = left[0].replace("(","", 1)
    left[-1] = left[-1].replace(")","", 1)
    return left, right

def strip_options(_list):
    option_pattern = re.compile(r'^[-]{2}.+')
    main_command, sentence = _list
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

def into_prefix(sentence, value_list, infix_functors = ['and','or','imp']):
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
    return sentence

def strip(_list, value_dict, isreversed=False):
    ''' Converts a `list` into a data tree 
        DO NOT USE'''
    names = []
    for i in _list:
        name = i[:]
        name = name.replace('(', '').replace(')', '')
        names.append(name)
    if len(names) == 1 and names[0] in value_dict.keys():
        return Sentence(names[0], value_dict[names[0]])
    else:
        brackets = 0
        for i in range(len(_list)):
            brackets += _list[i].count("(") * (-1)**isreversed
            brackets -= _list[i].count(")") * (-1)**isreversed
            if brackets <= 1 and names[i] in TREE_DICT.keys():
                if TREE_DICT[names[i]]==Negation:
                    if isreversed:
                        _list.reverse() 
                    right = strip(_list[i+1:], value_dict) # nie działa rozpisywanie segmentu ((not p) or
                    return Negation('not '+str(right), None, right)
                else:
                    leftlist = _list[0:i]; leftlist.reverse() # Creating a list for objects on the left side of the functor
                    left = strip(leftlist, value_dict, isreversed=True)
                    right = strip(_list[i+1:], value_dict)
                    return TREE_DICT[names[i]](str(right)+" "+names[i]+" "+str(left), None, left, right)



############### __main__ ###############
if __name__ == "__main__":
    for _dict in [{'p':False,'q':True}, {'p':True,'q':True}, {'p':False,'q':False}, {'p':True,'q':False}]:
        zdanie = '(p and q) -> ((not p) or (not q))' #nie działa xD
        #wynik = strip(zdanie.split(), _dict)
        #print(wynik.evaluate())
        print(into_prefix(syntax_analysis(zdanie.split()), _dict))
        break
