class BinaryTreeNode(object):

    def __init__(self):
        """按照定义，初始化为空树"""
        self.value = None
        self.left = None
        self.right = None

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


class ExpressionTreeNode(BinaryTreeNode):

    def inorder_expression(self):
        if self.has_left() and not self.left.is_empty():  # 这里偷懒了
            exp = ' '.join([self.left.inorder_expression(), self.value, self.right.inorder_expression()])
            return '(' + exp + ')'
        else:
            return self.value


class SearchTree(BinaryTreeNode):

    def insert(self, x) -> 'SearchTree':
        if self.is_empty():
            self.set_value(x)
            return self
        elif x < self.value:
            if not self.has_left():
                self.left = self.__class__()
            return self.left.insert(x)
        elif x > self.value:
            if not self.has_right():
                self.right = self.__class__()
            return self.right.insert(x)

    def find(self, x) -> 'SearchTree':
        if self.is_empty():
            return self
        elif x < self.value:
            return self.left.find(x)
        elif x > self.value:
            return self.right.find(x)
        else:
            return self

    def find_min(self) -> 'SearchTree':
        """递归版本"""
        if self.has_left() and not self.left.is_empty():
            return self.left.find_min()
        else:
            return self

    def find_max(self) -> 'SearchTree':
        """循环版本"""
        node = self
        while node.right is not None and not node.right.is_empty():
            node = node.right
        return node
