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


def shell_sort(array: List[int]):
    return


def heap_sort(array: List[int]):
    h = []
    for v in array:
        heapq.heappush(h, v)
    for i in range(len(array)):
        array[i] = heapq.heappop(h)
    return array


def merge_sort(array: List[int]):
    return


def quick_sort(array: List[int]):
    return
