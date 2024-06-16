import os
from huffman_arpeggio.core import build_huffman_tree
from huffman_arpeggio.visualization import visualize_huffman_tree


def test_visualize_huffman_tree():
    count_dict = {"A": 5, "B": 7, "C": 10}
    symbols = ["X", "O"]
    root = build_huffman_tree(count_dict, symbols)

    output_path = "tests/output/huffman_tree"
    visualize_huffman_tree(root, output_path)

    # Check if the file was created
    assert os.path.exists(f"{output_path}.png")

    # Cleanup
    os.remove(f"{output_path}.png")
    os.rmdir("tests/output")
