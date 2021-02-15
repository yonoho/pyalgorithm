import pytest

from . import main


@pytest.fixture
def weighted_charset():
    charset = [
        ('a', 10),
        ('e', 15),
        ('i', 12),
        ('s', 3),
        ('t', 4),
        (' ', 13),
        ('\n', 1),
    ]
    return charset


class TestGreedy(object):

    def test_huffman_code(self, weighted_charset):
        weights = dict(weighted_charset)
        codes = main.huffman_code(weighted_charset)
        assert sum([weights[char] * len(code) for char, code in codes.items()]) == 146
