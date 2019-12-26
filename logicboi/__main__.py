from .cnf import create as build_cnf
from .tree import build4values as build_tree
from .tree import gen_values, TREE_LIST
from .core import syntax_analysis, strip_options, getargs, into_prefix
from sys import argv as command

what_do = strip_options(command)

# Option searching
if what_do[0]=='tautotest':
    sent = syntax_analysis(what_do[1])
    args = getargs(sent, TREE_LIST)

    solution = True
    zdanienew = into_prefix(sent)
    for _dict in gen_values(args):
        solution &= build_tree(zdanienew, args)
    print("It's "+(not solution)*"not "+"a tautology")
elif what_do[0]=='contrtest':
    args = set()
    sent = syntax_analysis(what_do[1])
    nobrackets = [j.replace("(","").replace(")","") for j in sent]
    for i in nobrackets:
        if not i in TREE_LIST:
            args.update(i)

    solution = True
    zdanienew = into_prefix(sent)
    for _dict in gen_values(args):
        solution &= not build_tree(zdanienew, args)
    print("It's "+(not solution)*"not "+"a contrtautology")
elif what_do[0]=='cnf':
    build_cnf(syntax_analysis(what_do[1]))
else:
    print('Operation not found, consult with the readme')