# $ pytest -sv
# $ pytest -sv -m "not debug"
# $ pytest -sv -m "not debug" --pdb
import random
import pytest
from typing import Tuple, List
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

    def init_with_range(self, n: int) -> Tuple[SearchTreeNode, List[int]]:
        variables = list(range(n))
        random.shuffle(variables)
        t = SearchTreeNode()
        for x in variables:
            t.insert(x)
        return t, variables

    def test_find(self):
        t, variables = self.init_with_range(10)
        for x in variables:
            assert t.find(x).value == x
        assert t.find_min().value == min(variables)
        assert t.find_max().value == max(variables)

    def test_iter(self):
        n = 10
        t, variables = self.init_with_range(n)
        assert list(t.preorder_iter()) == sorted(variables)

    def test_delete(self):
        n = 10
        t, variables = self.init_with_range(n)
        for i, x in enumerate(variables):
            t = t.delete(x)
            if t:
                assert list(t.preorder_iter()) == sorted(variables[i + 1:])


class TestAvlTree(object):

    def init_with_range(self, n: int) -> Tuple[AvlTreeNode, List[int]]:
        variables = list(range(n))
        random.shuffle(variables)
        t = AvlTreeNode()
        for x in variables:
            t.insert(x)
        return t, variables

    @pytest.mark.debug
    def test_rotate(self):
        n = 20
        t, variables = self.init_with_range(n)
        t.print()
        t = t.rotate_to_left()
        t.print()
        t = t.rotate_to_right()
        t.print()

    def test_balance(self):
        n = 20
        t, variables = self.init_with_range(n)
        assert t.is_balanced()
        t.print()
