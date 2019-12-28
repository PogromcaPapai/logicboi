from functools import reduce
import regex
from sys import argv as command
import os
import core.table as tab

def get_key(my_dict, val): 
    ''' Gets key for a value '''
    for key, value in my_dict.items(): 
        if val == value: 
            return key 

############### Back End ###############

#### CNF ####

def encode(_list, arg_dict):
    SYNTAX_DICT = {'and':'a','or':'v','not':'n','imp':'vn'}
    
    SYNTAX_DICT.update(arg_dict)
    string = ''
    for i in _list:
        string += SYNTAX_DICT[i]
    return string

def reduce_negations(string):
    return string.replace("nn","")

def reduce_functors(string):
    return string

def internalize_alternatives(string):
    new = regex.sub(r'va(n?\d|(?>[va](?1)(?1)))((?1))((?1))',r'av\1\3v\2\3' , string)
    new = regex.sub(r'v(n?\d|(?>[va](?1)(?1)))a((?1))((?1))',r'av\1\2v\1\3' , new)
    return new

def de_morgan(string):
    new = regex.sub(r'na(n?\d|(?>[va](?1)(?1)))((?1))',r'vn\1n\2' , string)
    new = regex.sub(r'nv(n?\d|(?>[va](?1)(?1)))((?1))',r'an\1n\2' , new)
    return new

def is_end(sentence):
    matched = regex.fullmatch(r'(a((?1)(?1)|(?1)(?3)|(?3)(?1)|(?3)(?3)))|((v((?3)(?3)|(?3)n?\d|n?\d(?3)|n?\dn?\d))|n?\d)', sentence)
    return matched != None

def decode(string, arg_dict):
    SYNTAX_DICT = {'and':'a','or':'v','not':'n'}
    
    SYNTAX_DICT.update(arg_dict)
    new = []
    for i in string:
        new.append(get_key(SYNTAX_DICT, i))
    return new

def getresolution_list(list_string, args):
    new = []
    insert = set()
    or_count = 1
    negate = False
    for i in list_string:
        if i == 'or':
            or_count += 1
        elif i == 'and':
            pass
        elif i == 'not':
            negate = True
        elif i in args:
            or_count -= 1
            insert.add(negate*'~'+i)
            negate = False
            if or_count==0:
                new.append(insert)
                insert = set()
                or_count = 1
        else:
            raise Exception(f'Couldn\'t parse: {i}')
    return new

############### Sentence Parsing ###############


def cut(sentence, val):
    ''' Used in `into_prefix`, returns arguments of an infix functor '''
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

def syntax_analysis(sentence):
    ''' Converts functors into a standarized notation'''
    SYNTAX_DICT = {'oraz':'and', '&':'and', 
               'lub':'or', '+':'or', 
               '~':'not', 
               '->':'imp', '>':'imp'}

    new = []
    for i in sentence:
        for j in SYNTAX_DICT.keys():
            i = i.replace(j, SYNTAX_DICT[j])
        new.append(i)
    return new

def into_prefix(sentence, infix_functors = ['and','or','imp'], prefix_functors = ['not']):
    ''' Converts the sentence (list of words) into a prefix notation '''
    brackets = 0
    for i in range(len(sentence)):
            brackets += sentence[i].count("(")
            brackets -= sentence[i].count(")")
            assert brackets >= 0, "Brackets not opened"
            if sentence[i] in infix_functors and brackets==0:
                new = cut(sentence, i)
                right = into_prefix(new[1], infix_functors = infix_functors)
                left = into_prefix(new[0], infix_functors = infix_functors)
                return [sentence[i]]+left+right
            elif sentence[i] in prefix_functors and brackets==0:
                new = cut(sentence, 0)
                right = into_prefix(new[1], prefix_functors = prefix_functors)
                return [sentence[i]]+right
    return sentence


############### Front-End ###############

def strip_options(command):
    command_list = list(command[1:])
    option_pattern = regex.compile(r'^[-]{2}.+')
    main_command, *sentence = command_list
    options = []
    for word in sentence[:]:
        if option_pattern.match(word):
            sentence.remove(word)
            options.append(word)
    assert len(sentence)<=1, "Command not recognized: "+sentence
    if len(sentence)==0:
        ############|Write your sentence here for constant debuging
        string_sent = ""
        ############|----------------------------------------------
        if string_sent=="":
            string_sent = input("Podaj zdanie: ")
    else:
        string_sent = sentence[0]
    return [main_command, string_sent.split(), options]

############### __main__ ###############
if __name__ == "__main__":
    if len(command)==1:
        raise Exception("Enter a full command")    
    what_do = strip_options(command)

    # Option searching
    if what_do[0]=='help':
        pass
    elif what_do[0]=='tautotest':
        args = set()
        sent = syntax_analysis(what_do[1])
        nobrackets = [j.replace("(","").replace(")","") for j in sent]
        for i in nobrackets:
            if not i in tab.TREE_DICT.keys():
                args.update(i)

        solution = True
        for _dict in tab.gen_values(args):
            zdanienew = into_prefix(sent)
            tree = tab.parse(zdanienew, _dict)
            solution &= tree.evaluate()
        print("It's "+(not solution)*"not "+"a tautology")
    elif what_do[0]=='contrtest':
        args = set()
        sent = syntax_analysis(what_do[1])
        nobrackets = [j.replace("(","").replace(")","") for j in sent]
        for i in nobrackets:
            if not i in tab.TREE_DICT.keys():
                args.update(i)

        solution = True
        for _dict in tab.gen_values(args):
            zdanienew = into_prefix(sent)
            tree = tab.parse(zdanienew, _dict)
            solution &= not tree.evaluate()
        print("It's "+(not solution)*"not "+"a contrtautology")
    elif what_do[0]=='cnf':
        args = dict()
        sent = syntax_analysis(what_do[1])
        nobrackets = [j.replace("(","").replace(")","") for j in sent]
        j = 0
        for i in nobrackets:
            if not (i in tab.TREE_DICT.keys() or i in args.keys()):
                args[i] = str(j)
                j += 1
        assert j<10, "Maksymalna liczba zmiennych zdaniowych to 10"
        zdanienew = into_prefix(sent)
        ready4cnf = encode(zdanienew, args)
        
        # Solving
        cnf = reduce_functors(ready4cnf[:])
        while not is_end(cnf):
            cnf = reduce_negations(cnf)
            cnf = de_morgan(cnf)
            cnf = internalize_alternatives(cnf)
            print(cnf)
        finished = decode(cnf, args)
        print(finished)
        print(getresolution_list(finished, args.keys()))

    else:
        print('Operation not found, consult with the readme')