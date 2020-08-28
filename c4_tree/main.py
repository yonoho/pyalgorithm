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

    def set_value(self, x):
        """子树非空，因此这里不设置 left 和 right 的值"""
        self.value = x

    def is_empty(self) -> bool:
        """空树的定义"""
        return self.value is None

    def has_left(self) -> bool:
        return self.left is not None

    def has_right(self) -> bool:
        return self.right is not None

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
                self.left = self.__class__()
                self.left.parent = self
            return self.left.insert(x)
        elif x > self.value:
            if not self.has_right():
                self.right = self.__class__()
                self.right.parent = self
            return self.right.insert(x)

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
    def rotate_to_right(self):
        """left node rise"""
        return

    def rotate_to_left(self):
        """right node rise"""
        return
