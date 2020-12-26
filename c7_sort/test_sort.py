# $ pytest -sv
import random
import pytest
from .main import *

SAMPLE_NUM = 1000
SAMPLE_RANGE = 10 ** 10


@pytest.fixture
def rand_int_array():
    return [int(random.random() * SAMPLE_RANGE) for i in range(SAMPLE_NUM)]


class TestSort(object):

    def assert_sorted(self, int_array):
        for i in range(len(int_array) - 1):
            assert int_array[i] <= int_array[i + 1]

    def test_insertion_sort(self, rand_int_array):
        insertion_sort(rand_int_array)
        self.assert_sorted(rand_int_array)

    # def test_shell_sort(self, rand_int_array):
    #     shell_sort(rand_int_array)
    #     self.assert_sorted(rand_int_array)

    def test_heap_sort(self, rand_int_array):
        heap_sort(rand_int_array)
        self.assert_sorted(rand_int_array)

    def test_merge_sort(self, rand_int_array):
        merge_sort(rand_int_array)
        self.assert_sorted(rand_int_array)

    def test_quick_sort(self, rand_int_array):
        quick_sort(rand_int_array)
        self.assert_sorted(rand_int_array)
