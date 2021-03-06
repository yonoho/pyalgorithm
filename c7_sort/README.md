为了方便，本文描述的排序算法都基于以下假设：

- 排序对象为整数数组
- 排序对象都可以放入内存，排序过程也没有内存限制

排序就是让数组产生 “序” 的过程。后面会证明：任何基于比较的算法都需要至少 `N*Log(N)` 次比较。因此算法效率的主要关注点就是比较次数，尽量不要做重复的比较。空间效率相对不那么关心，因为这些算法都可以写成直接交换式而不产生显著的额外内存消耗。

# 分析

### 排序的一般下界

决策树（decision tree）是证明这个下界的抽象概念。决策树的节点代表所有可能的决策，边代表某条已知条件。某个节点所有已知的条件包含从该节点到根的全部边。叶子节点只包含一种决策，即在所有已知条件下，作出的最终决策。

在排序算法里，决策树的节点代表**在已知条件下数组可能的排列**，两条边代表两个元素比较的结果（因此这里的决策树是二叉树）。叶子结点代表一种固定的排序。举例含有两个元素的决策树：根节点是 `[a, b] / [b, a]`，其左边是 `a < b`，左子节点就是 `[a, b]`，右边是 ` a > b`，右子节点是 `[b, a]`。

存在以下定理：

- 具有 L 个叶子节点的决策树深度至少是 Log(L)。
- 因为具有 N 个元素的决策树必然有 N! 个叶子节点，它的决策树深度至少是 Log(N!)。
- Log(N!) = Ω(N*Log(N))。证明略。

# 算法

### 插入排序

插入排序是最简单直观的排序方式，我们从前向后遍历元素，确保该元素位置之前的切片是排过序的。具体方法为向前比较，如果逆序则交换元素。

显然它的复杂度是 O(N^2)，且这个极限在完全逆序输入时是可以达到的。这个算法慢的地方在于它只比较和交换相邻的元素，即把一个新元素插入已排序数组的过程是 O(N) 的。

这个复杂度对任意只通过交换相邻元素来进行排序的算法都适用。证明过程需要定义一个概念为 **逆序**(inversion)，指的是任意两个位置不符合排序要求的元素。注意 [3, 2, 1] 这样的数组逆序数为 3。只交换相邻元素的算法每次只能消除一个逆序。存在以下定理：

- N 个互异数的数组，平均逆序数是 N(N-1)/4。考虑数组排列可证明。

### 归并排序（mergesort）

归并排序以最坏 `O(NlogN)` 情形运行，其基本操作是合并两个已排序的表，已排序的子表来自于递归调用的归并排序，递归的基准情形是表里元素小于 2 的时候。

### 快速排序（quicksort）

快排的算法和归并很类似，都是基于分治（devide and conquer）策略。与分治的二分法不同，快排的规则是先选定一个“中值”（pivot）然后把数组分成小于 pivot 和 大于 pivot 两组并分置在 pivot 两边，最后递归排序两个子组。

快排看起来复杂度与归并一样，且存在两组大小不一致的问题。但实际上却跑起来更快，原因是分组操作的实现方法十分高效，它像插入排序一样只做本地交换。

### 选择 pivot 的方法

最佳 pivot 是中值，但为了避免在找中值上花的时间过多，我们会把算法简化，并避免最坏情形。这里使用“三数中值分割法”（Median-of-three Partitiononing）。即在数组索引的首位、末位、中位的三个值中取中位数。

### 分割方法

这里将要介绍的就是让快排跑的比归并更快的方法。我们的目标是：让 pivot 位于数组的某个位置，使其前面的元素全都小于它，其后面元素全都大于它。过程期望：直接在本地交换，不使用临时数组；尽可能减少交换的次数。显然存在两点事实：

1. pivot 的位置是浮动的，因为数组内的元素未知。
2. 实现最少交换的必要条件是：后移的元素比左移的元素大，在此基础上，后移的元素应该比 pivot 大，否则它就没有必要后移，前移的元素也应该比 pivot 小，否则没必要前移。

因此规则为：

1. 先将 pivot 从数组中移出去，具体方法可以是和第一个或最后一个元素交换
2. 对剩余的 N-1 数组，从前向后和从后向前分别遍历元素。向后的遍历过程跳过小于 pivot 的元素，停止时的元素记为 i；向前的遍历过程跳过大于 pivot 的元素，停止时的元素记为 j。除了比较 pivot 会停止外，前后遍历相交时也会停止。后一种情况下显然排序完成。
3. 当遍历过程因为前一种情况停止时，必然存在 `i >= j`，此时交换两个元素即可，然后继续遍历。直到后一种情况发生。
4. 把 pivot 放回到遍历交汇的位置。

### 遍历过程如何处理等于 pivot 的情况

即，应该停止等待交换还是跳过。答案是停止，因为如果跳过，则很容易把连续的 pivot 值全都归到一边。在最坏清醒下会导致 O(N^2) 的复杂度。

### 小数组

对于小数组(N<=20)，快排的表现不如其他算法好，比如插入排序。因此当数组变小时，应该替换排序算法。

### 桶式排序

如果排序方法不限定基于比较，那么有可能存在更快的方法，比如桶式排序。这要求已知数组元素各不相交且都小于桶大小。

### 外部排序

外部排序的核心问题是合并，因为现在硬件已经发生了很大变化，原文中针对磁带的排序方法未必适用于已经普及的 SSD，这里就先略过。
