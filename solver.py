from exprtree import *
from copy import deepcopy

solutions = set()

def solve(nodes):
    if len(nodes) == 1:
        val, expr = nodes[0].eval_node()
        if val == 24:
            solutions.add(expr)
    else:
        L = len(nodes)
        ops = ('+', '-', '*', '/')
        for i1 in range(L):
            for i2 in range(L):
                if i1 != i2:
                    for op in ops:
                        if op in ('-', '/') or i1 < i2:
                            nodes_copy = deepcopy(nodes) # the original list won't be affected
                            new_nodes = [nodes_copy[k] for k in range(L) if k not in (i1, i2)]
                            node1 = nodes_copy[i1]
                            node2 = nodes_copy[i2]
                            new_nodes.append(ExprTreeNode(op, node1, node2))
                            solve(new_nodes)


input_str = input('Please insert 4 integers, each within [1,13], separated by space:\n')
# check input validity
assert len(input_str.split()) == 4, 'number of entries should be 4'
for entry in input_str.split():
    assert isinstance(eval(entry), int), 'entries should be integers'
    assert 1 <= int(entry) <= 13, 'entry values should be within [1,13]'

nums = [int(x) for x in input_str.split()]
nums = sorted(nums)
nodes = [ExprTreeNode(num) for num in nums]

solve(nodes)

for solution in solutions:
    print ('%s = %d' % (solution, 24))
