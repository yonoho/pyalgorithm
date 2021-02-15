from typing import Dict, List, Tuple


def huffman_code(weighted_charset: List[Tuple[str, int]]) -> Dict[str, str]:
    weighted_charset.sort(key=lambda x: x[1])
    trees = []
    for char, weight in weighted_charset:
        trees.append({'v': char, 'w': weight})
    while len(trees) > 1:
        new_tree = {'l': trees[0], 'r': trees[1], 'w': trees[0]['w'] + trees[1]['w']}
        trees = trees[2:] + [new_tree]
        trees.sort(key=lambda x: x['w'])
    return scan_code_tree(trees[0])


def scan_code_tree(tree: dict, parent_codes: List[str] = []):
    codes = {}
    if tree.get('l'):
        codes.update(scan_code_tree(tree['l'], parent_codes + ['0']))
    if tree.get('r'):
        codes.update(scan_code_tree(tree['r'], parent_codes + ['1']))
    if tree.get('v'):
        codes[tree['v']] = ''.join(parent_codes)
    return codes
