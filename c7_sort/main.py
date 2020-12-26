import heapq
from typing import List


def insertion_sort(array: List[int]):
    for i, v in enumerate(array):
        for j in range(i - 1, -1, -1):
            if v < array[j]:
                array[j], array[j + 1] = array[j + 1], array[j]
            else:
                break
    return array


# def shell_sort(array: List[int]):
#     return


def heap_sort(array: List[int]):
    h = []
    for v in array:
        heapq.heappush(h, v)
    for i in range(len(array)):
        array[i] = heapq.heappop(h)
    return array


def _merge_two(a: List[int], b: List[int]) -> List[int]:
    c = []
    idx_a, idx_b = 0, 0
    while idx_a < len(a) and idx_b < len(b):
        if a[idx_a] < b[idx_b]:
            c.append(a[idx_a])
            idx_a += 1
        else:
            c.append(b[idx_b])
            idx_b += 1
    c.extend(a[idx_a:])
    c.extend(b[idx_b:])
    return c


def merge_sort(array: List[int]):
    if len(array) >= 2:
        mid_idx = len(array) // 2
        for i, v in enumerate(_merge_two(merge_sort(array[:mid_idx]),
                                         merge_sort(array[mid_idx:]))):
            array[i] = v
    return array


def quick_sort(array: List[int]):
    if len(array) <= 3:
        return insertion_sort(array)
    pivot, pivot_idx = sorted([(array[0], 0),
                               (array[-1], len(array) - 1),
                               (array[len(array) // 2], len(array) // 2)])[1]
    array[pivot_idx], array[-1] = array[-1], array[pivot_idx]
    i, j = 0, len(array) - 2
    while i < j:
        while array[i] < pivot and i < j:
            i += 1
        while array[j] > pivot and j > i:
            j -= 1
        if array[i] > array[j]:
            array[i], array[j] = array[j], array[i]
        elif array[i] == array[j]:
            pass
        else:
            break
    array[i], array[-1] = array[-1], array[i]
    # array[i] is now the pivot
    # As slice creates shallow copy, here we use assignments
    array[:i] = quick_sort(array[:i])
    array[i + 1:] = quick_sort(array[i + 1:])
    return array
