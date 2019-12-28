import regex

def get_key(my_dict, val): 
    ''' Gets key for a value '''
    for key, value in my_dict.items(): 
        if val == value: 
            return key 

#### Back-End ####

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

#### Front-End ####

def encode(_list, arg_dict):
    SYNTAX_DICT = {'and':'a','or':'v','not':'n','imp':'vn'}
    
    SYNTAX_DICT.update(arg_dict)
    string = ''
    for i in _list:
        string += SYNTAX_DICT[i]
    return string

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