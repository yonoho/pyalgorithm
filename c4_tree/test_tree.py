# $ pytest -sv
import random
from .main import *


class TestExpressionTree(object):

    def test(self):
        n1 = ExpressionTreeNode()
        n1.set_value('+')
        n1.left = ExpressionTreeNode()
        n1.left.set_value('1')
        n1.right = ExpressionTreeNode()
        n1.right.set_value('2')
        n2 = ExpressionTreeNode()
        n2.set_value('-')
        n2.left = ExpressionTreeNode()
        n2.left.set_value('3')
        n2.right = ExpressionTreeNode()
        n2.right.set_value('4')
        n = ExpressionTreeNode()
        n.set_value('/')
        n.left = n1
        n.right = n2
        assert n.inorder_expression() == '((1 + 2) / (3 - 4))'


class TestSearchTree(object):

    def test_find(self):
        variables = list(range(10))
        random.shuffle(variables)
        t = SearchTree()
        for x in variables:
            t.insert(x)
        for x in variables:
            assert t.find(x).value == x
        assert t.find_min().value == min(variables)
        assert t.find_max().value == max(variables)

    def test_delete(self):
        pass
