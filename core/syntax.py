import regex

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
            brackets -= sentence[i].count(")")
    return sentence

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