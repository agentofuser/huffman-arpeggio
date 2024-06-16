import pytest
from huffman_arpeggio.core import (
    Node,
    calculate_padding,
    merge_nodes,
    build_huffman_tree,
    generate_encoding_map_with_count,
)


def test_calculate_padding():
    assert calculate_padding(10, 3) == (5, 1)
    assert calculate_padding(5, 2) == (4, 0)


def test_merge_nodes():
    nodes = [Node(5, "A"), Node(7, "B"), Node(10, "C")]
    root = merge_nodes(nodes, 2)
    assert root.count == 22
    assert len(root.children) == 2


def test_build_huffman_tree():
    count_dict = {"A": 5, "B": 7, "C": 10}
    symbols = ["X", "O"]
    root = build_huffman_tree(count_dict, symbols)
    assert root is not None
    assert root.count == 22

    # Test invalid inputs
    with pytest.raises(ValueError):
        build_huffman_tree({}, symbols)

    with pytest.raises(ValueError):
        build_huffman_tree(count_dict, [])

    with pytest.raises(ValueError):
        build_huffman_tree(count_dict, ["X", "X"])


def test_generate_encoding_map_with_count():
    count_dict = {"A": 5, "B": 7, "C": 10}
    symbols = ["X", "O"]
    root = build_huffman_tree(count_dict, symbols)
    encoding_map = generate_encoding_map_with_count(root, symbols, count_dict)

    # Check the keys and their corresponding values
    assert encoding_map[("X",)] == ("C", 10)
    assert encoding_map[("O", "X")] == ("A", 5)
    assert encoding_map[("O", "O")] == ("B", 7)
