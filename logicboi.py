import regex
from sys import argv as command
import os
import core.table as tab
import core.cnf as cnf
import core.syntax as syn
import time

if __name__ == "__main__":
    if len(command)==1:
        new = input("Podaj komendę: ")
        if len(new)==0:
            raise Exception("Enter a full command")    
        else:
            command.append(new)
    what_do = syn.strip_options(command)

    # Option searching
    if what_do['main']=='help':
        pass
    elif what_do['main']=='tautotest':
        args = set()
        sent = syn.syntax_analysis(what_do['string'])
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
    elif what_do['main']=='contrtest':
        args = set()
        sent = syn.syntax_analysis(what_do['string'])
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
    elif what_do['main']=='cnf':
        args = dict()
        sent = syn.syntax_analysis(what_do['string'])
        nobrackets = [j.replace("(","").replace(")","") for j in sent]
        j = 0
        for i in nobrackets:
            if not (i in tab.TREE_DICT.keys() or i in args.keys()):
                args[i] = str(j)
                j += 1
        assert j<10, "Maksymalna liczba zmiennych zdaniowych to 10"
        elapsed = time.perf_counter_ns()
        zdanienew = syn.into_prefix(sent)
        ready4cnf = cnf.encode(zdanienew, args)
        
        # Solving
        cnfstring = cnf.reduce_functors(ready4cnf[:])
        while not cnf.is_end(cnfstring):
            cnfstring = cnf.reduce_negations(cnfstring)
            cnfstring = cnf.de_morgan(cnfstring)
            cnfstring = cnf.internalize_alternatives(cnfstring)
            #print(cnfstring)
        finished = cnf.decode(cnfstring, args)
        for i in cnf.getresolution_list(finished, args.keys()):
            print(sorted(i, key=cnf.sortval))
        # performance checking code 
        if '--debug' in what_do['options']:
            print((time.perf_counter_ns() - elapsed)/(10**9))
    else:
        print('Operation not found, consult with the readme')