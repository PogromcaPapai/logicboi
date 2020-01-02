import regex
from sys import argv as command
import os
import core.table as tab
import core.cnf as cnf
import core.syntax as syn

if __name__ == "__main__":
    if len(command)==1:
        raise Exception("Enter a full command")    
    what_do = syn.strip_options(command)

    # Option searching
    if what_do[0]=='help':
        pass
    elif what_do[0]=='tautotest':
        args = set()
        sent = syn.syntax_analysis(what_do[1])
        nobrackets = [j.replace("(","").replace(")","") for j in sent]
        for i in nobrackets:
            if not i in tab.TREE_DICT.keys():
                args.update(i)

        solution = True
        for _dict in tab.gen_values(args):
            zdanienew = syn.into_prefix(sent)
            tree = tab.parse(zdanienew, _dict)
            solution &= tree.evaluate()
        print("It's "+(not solution)*"not "+"a tautology")
    elif what_do[0]=='contrtest':
        args = set()
        sent = syn.syntax_analysis(what_do[1])
        nobrackets = [j.replace("(","").replace(")","") for j in sent]
        for i in nobrackets:
            if not i in tab.TREE_DICT.keys():
                args.update(i)

        solution = True
        for _dict in tab.gen_values(args):
            zdanienew = syn.into_prefix(sent)
            tree = tab.parse(zdanienew, _dict)
            solution &= not tree.evaluate()
        print("It's "+(not solution)*"not "+"a contrtautology")
    elif what_do[0]=='cnf':
        args = dict()
        sent = syn.syntax_analysis(what_do[1])
        nobrackets = [j.replace("(","").replace(")","") for j in sent]
        j = 0
        for i in nobrackets:
            if not (i in tab.TREE_DICT.keys() or i in args.keys()):
                args[i] = str(j)
                j += 1
        assert j<10, "Maksymalna liczba zmiennych zdaniowych to 10"
        zdanienew = syn.into_prefix(sent)
        ready4cnf = cnf.encode(zdanienew, args)
        
        # Solving
        cnfstring = cnf.reduce_functors(ready4cnf[:])
        while not cnf.is_end(cnfstring):
            cnfstring = cnf.reduce_negations(cnf)
            cnfstring = cnf.de_morgan(cnf)
            cnfstring = cnf.internalize_alternatives(cnf)
            print(cnfstring)
        finished = cnfstring.decode(cnfstring, args)
        print(cnf.getresolution_list(finished, args.keys()))

    else:
        print('Operation not found, consult with the readme')