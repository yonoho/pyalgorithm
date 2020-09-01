from typing import Tuple


class EmptyTreeError(Exception):
    """因为是空树，而无法执行某些操作"""
    pass


class BinaryTreeNode(object):

    def __init__(self):
        """按照定义，初始化为空树"""
        self.value = None
        self.left = None
        self.right = None
        self.parent = None

    def __repr__(self):
        return '%s: %d' % (self.__class__, self.value)

    def set_value(self, x):
        """子树非空，因此这里不设置 left 和 right 的值"""
        self.value = x

    def is_empty(self) -> bool:
        """空树的定义"""
        return self.value is None

    def has_left(self) -> bool:
        return self.left is not None

    def set_left(self, node):
        """允许 set None"""
        self.left = node
        if node:
            node.parent = self

    def has_right(self) -> bool:
        return self.right is not None

    def set_right(self, node):
        """允许 set None"""
        self.right = node
        if node:
            node.parent = self

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    @property
    def height(self):
        if self.is_leaf():
            return 0
        elif self.has_left() and self.has_right():
            return max([self.left.height, self.right.height]) + 1
        elif self.has_left():
            return self.left.height + 1
        else:
            return self.right.height + 1

    def gen_2d_coordinates(self, idx=0, depth=0):
        """生成一个二维表"""
        if self.has_left() and not self.left.is_empty():
            yield from self.left.gen_2d_coordinates(idx - 1, depth + 1)
        yield idx, depth, self.value
        if self.has_right() and not self.right.is_empty():
            yield from self.right.gen_2d_coordinates(idx + 1, depth + 1)

    def gen_2d_table(self):
        coordinates = list(self.gen_2d_coordinates())
        rows = [r[0] for r in coordinates]
        cols = [r[1] for r in coordinates]
        width = max(rows) - min(rows) + 1
        depth = max(cols) + 1
        table = [[None for j in range(width)] for i in range(depth)]
        for idx, depth, value in coordinates:
            table[depth][idx - min(rows)] = value
        return table

    def print(self):
        table = self.gen_2d_table()
        depth = len(table)
        width = len(table[0])
        col_widths = []
        for i in range(width):
            max_value = 0
            for j in range(depth):
                if table[j][i]:
                    max_value = max([max_value, table[j][i]])
            col_widths.append(len(str(max_value)))
        print('')
        for row in table:
            for i, v in enumerate(row):
                row[i] = '%*d' % (col_widths[i], v) if v else ' ' * col_widths[i]
            print(''.join(row))


class ExpressionTreeNode(BinaryTreeNode):

    def inorder_expression(self):
        if self.has_left() and not self.left.is_empty():  # 这里偷懒了
            exp = ' '.join([self.left.inorder_expression(), self.value, self.right.inorder_expression()])
            return '(' + exp + ')'
        else:
            return self.value


class SearchTreeNode(BinaryTreeNode):

    def __init__(self):
        super().__init__()
        self.counter = 0  # 重复插入用计数实现，但删除是实时删除（非懒删除）

    def set_value(self, x) -> 'SearchTreeNode':
        super().set_value(x)
        self.counter += 1

    def insert(self, x) -> 'SearchTreeNode':
        if self.is_empty():
            self.set_value(x)
            return self
        elif x < self.value:
            if not self.has_left():
                self.set_left(self.__class__())
            return self.left.insert(x)
        elif x > self.value:
            if not self.has_right():
                self.set_right(self.__class__())
            return self.right.insert(x)
        else:
            return self

    def find(self, x) -> 'SearchTreeNode':
        if self.is_empty():
            return self
        elif x < self.value:
            return self.left.find(x)
        elif x > self.value:
            return self.right.find(x)
        else:
            return self

    def preorder_iter(self):
        if self.is_empty():
            raise StopIteration()
        if self.has_left():
            yield from self.left.preorder_iter()
        for i in range(self.counter):
            yield self.value
        if self.has_right():
            yield from self.right.preorder_iter()

    def find_min(self) -> 'SearchTreeNode':
        """递归版本"""
        if self.has_left() and not self.left.is_empty():
            return self.left.find_min()
        else:
            return self

    def find_max(self) -> 'SearchTreeNode':
        """循环版本"""
        node = self
        while node.right is not None and not node.right.is_empty():
            node = node.right
        return node

    def delete(self, x) -> 'SearchTreeNode':
        """删除可能导致子树变化，因此需要赋值操作，返回的是新子树的根"""
        if self.is_empty():
            raise EmptyTreeError()
        if x < self.value:
            self.left = self.left.delete(x)
        elif x > self.value:
            self.right = self.right.delete(x)
        else:
            if self.counter > 1:
                self.counter -= 1
            else:
                if self.is_leaf():
                    return None
                if self.has_left() and self.has_right():
                    # 随意选择了左子树的最大节点
                    new_node = self.left.find_max()
                    new_node.left = self.left.delete(new_node.value)
                    new_node.right = self.right
                    return new_node
                return self.left or self.right
        return self


class AvlTreeNode(SearchTreeNode):
    def rotate_to_right(self) -> 'AvlTreeNode':
        """left node rise"""
        if not self.left:
            raise ValueError('Can not rotate to right while left node non-exists.')
        new_root = self.left
        # 先过继
        self.set_left(new_root.right)
        # 再旋转
        new_root.set_right(self)
        new_root.parent = None
        return new_root

    def rotate_to_left(self) -> 'AvlTreeNode':
        """right node rise"""
        if not self.right:
            raise ValueError('Can not rotate to left while right node non-exists.')
        new_root = self.right
        # 先过继
        self.set_right(new_root.left)
        # 再旋转
        new_root.set_left(self)
        new_root.parent = None
        return new_root

    def is_balanced(self) -> bool:
        """只检查当前结点"""
        if self.is_empty():
            return True
        left_height = self.left.height + 1 if self.has_left() else 0
        right_height = self.right.height + 1 if self.has_right() else 0
        return abs(left_height - right_height) < 2

    def balanced_insert(self, x) -> Tuple['AvlTreeNode', 'AvlTreeNode']:
        """因为可能造成树的旋转，因此返回 (new_node, root)"""
        ret = self.insert(x)
        check_node = ret.parent or ret
        while check_node:
            if not check_node.is_balanced():
                parent_node = check_node.parent
                rebalanced_node = check_node.rebalance()
                if parent_node:
                    side = 'left' if check_node.value < parent_node.value else 'right'
                    getattr(parent_node, 'set_%s' % side)(rebalanced_node)
            if check_node.parent:
                check_node = check_node.parent
            else:
                break
        return ret, check_node

    def rebalance(self) -> 'AvlTreeNode':
        if self.has_left() and self.left.height == self.height - 1:
            if self.left.has_left() and self.left.left.height == self.height - 2:
                return self.rotate_to_right()
            else:
                self.set_left(self.left.rotate_to_left())
                return self.rotate_to_right()
        else:
            if self.right.has_right() and self.right.right.height == self.height - 2:
                return self.rotate_to_left()
            else:
                self.set_right(self.right.rotate_to_right())
                return self.rotate_to_left()
