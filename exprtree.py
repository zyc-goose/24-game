from fractions import Fraction
from mybool import MyBool

T1 = ('+', '-')
T2 = ('*', '/')

class ExprTreeNode:

    def __init__(self, val, left=None, right=None):
        self.mark = {}
        self.mark['-'] = MyBool(False)
        self.mark['/'] = MyBool(False)
        if isinstance(val, (int, Fraction)):
            self.val = Fraction(val)
            self.T = 0
        elif val in T1:
            self.val = '+'
            self.T = 1
            self.rank = 1
            if val == '-':
                self.rank = 2
                right.mark['-'].flip()
                right._pushdown()
            if left.T == 1:
                self.opnds = left.opnds.copy()  # operands
            else:
                self.opnds = [left]
            if right.T == 1:
                self.opnds.extend(right.opnds)
            else:
                self.opnds.append(right)
            self.opnds.sort()
        elif val in T2:
            self.val = '*'
            self.T = 2
            self.rank = 1
            if val == '/':
                self.rank = 2
                right.mark['/'].flip()
                right._pushdown()
            if left.T == 2:
                self.opnds = left.opnds.copy()
            else:
                self.opnds = [left]
            if right.T == 2:
                self.opnds.extend(right.opnds)
            else:
                self.opnds.append(right)
            self.opnds.sort()

    def eval_node(self):
        """Evaluate the value and expression of the node"""
        if self.T == 0:
            return self.val, str(self.val)
        exprs = []
        if self.T == 1:
            val_sum = 0
        else:
            val_sum = 1
        for opnd in self.opnds:
            val, expr = opnd.eval_node()
            if val is None:
                return None, None
            if self.T > opnd.T > 0:
                expr = '(' + expr + ')'
            if opnd.mark['-']:
                val_sum -= val
                expr = '-' + expr
            elif opnd.mark['/']:  # check for zero division
                if val == 0:
                    return None, None
                val_sum /= val
                expr = '/' + expr
            elif self.T == 1:
                val_sum += val
                expr = '+' + expr
            else:
                val_sum *= val
                expr = '*' + expr
            exprs.append(expr)
        exprs[0] = exprs[0][1:]
        return val_sum, ''.join(exprs)

    def _checkmark(self):
        """Check the existance of minus mark in self.opnds"""
        assert self.T == 1
        for opnd in self.opnds:
            if opnd.mark['-']:
                return True
        return False

    def _pushdown(self):
        """Push down the minus and division marks if possible"""
        if self.T == 1 and self.mark['-']:
            self.mark['-'].flip()
            for opnd in self.opnds:
                opnd.mark['-'].flip()
                opnd._pushdown()
            self.opnds.sort()
        if self.T == 2 and self.mark['-']:
            for opnd in filter(lambda obj: obj.T == 1, self.opnds):
                if opnd._checkmark():  # flip all children
                    self.mark['-'].flip()
                    for child in opnd.opnds:
                        child.mark['-'].flip()
                        child._pushdown()
                    opnd.opnds.sort()
                    break
            self.opnds.sort()
        if self.T == 2 and self.mark['/']:
            self.mark['/'].flip()
            for opnd in self.opnds:
                opnd.mark['/'].flip()
            self.opnds.sort()

    def _compare(self, other):
        if self.mark['-'] < other.mark['-']:
            return -1
        elif self.mark['-'] > other.mark['-']:
            return 1
        elif self.mark['/'] < other.mark['/']:
            return -1
        elif self.mark['/'] > other.mark['/']:
            return 1
        elif self.T < other.T:
            return -1
        elif self.T > other.T:
            return 1
        elif self.T == 0:
            return self.val - other.val
        elif self.rank != other.rank:
            return self.rank - other.rank
        else:
            for lhs, rhs in zip(self.opnds, other.opnds):
                diff = lhs._compare(rhs)
                if diff != 0:
                    return diff
            return len(self.opnds) - len(other.opnds)

    def __lt__(self, other):
        return self._compare(other) < 0

    def __eq__(self, other):
        return self._compare(other) == 0


# For testing
if __name__ == '__main__':
    n1 = ExprTreeNode(3)
    n2 = ExprTreeNode(3)
    n3 = ExprTreeNode(8)
    n4 = ExprTreeNode(8)
    nn1 = ExprTreeNode('-', n1, n2)
    nn2 = ExprTreeNode('-', n3, n4)
    root = ExprTreeNode('*', nn2, nn1)
    val, expr = root.eval_node()
    print ('%s = %s' % (expr, val))
    root = ExprTreeNode('*', nn2, nn1)
    val, expr = root.eval_node()
    print ('%s = %s' % (expr, val))
    root = ExprTreeNode('*', nn2, nn1)
    val, expr = root.eval_node()
    print ('%s = %s' % (expr, val))



