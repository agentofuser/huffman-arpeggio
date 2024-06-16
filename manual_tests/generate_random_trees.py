import os
import random
import string
from graphviz import Digraph
from huffman_arpeggio.core import Node, build_huffman_tree, calculate_padding


def generate_random_data(num_targets: int, max_count: int, num_symbols: int):
    """
    Generate random count_dict and symbols.

    :param num_targets: Number of targets in count_dict.
    :param max_count: Maximum count value for targets.
    :param num_symbols: Number of symbols for encoding.
    :return: A tuple (count_dict, symbols).
    """
    count_dict = {
        "".join(random.choices(string.ascii_uppercase, k=1)): random.randint(
            1, max_count
        )
        for _ in range(num_targets)
    }
    symbols = random.sample(string.ascii_uppercase, num_symbols)
    return count_dict, symbols


def test_random_trees(num_tests: int, output_dir: str):
    """
    Generate random Huffman trees and visualize them.

    :param num_tests: Number of random trees to generate.
    :param output_dir: Directory to save the visualizations.
    """
    for i in range(num_tests):
        num_targets = random.randint(2, 10)  # Random number of targets
        max_count = random.randint(1, 20)  # Random max count value
        num_symbols = random.randint(2, 5)  # Random number of symbols

        count_dict, symbols = generate_random_data(num_targets, max_count, num_symbols)
        root = build_huffman_tree(count_dict, symbols)

        output_path = f"{output_dir}/huffman_tree_{i}"
        num_branch_points, num_padding = calculate_padding(
            len(count_dict), len(symbols)
        )
        visualize_huffman_tree_with_data(
            root, output_path, count_dict, symbols, num_branch_points, num_padding
        )


def visualize_huffman_tree_with_data(
    root: Node,
    output_path: str,
    count_dict: dict,
    symbols: list,
    num_branch_points: int,
    num_padding: int,
):
    """
    Visualize the Huffman tree using Graphviz, embedding the count_dict, symbols,
    and padding calculation.

    :param root: The root of the Huffman tree.
    :param output_path: The path to save the output visualization file.
    :param count_dict: The count dictionary used to build the tree.
    :param symbols: The symbols used for encoding.
    :param num_branch_points: Number of branch points calculated.
    :param num_padding: Number of padding nodes calculated.
    """
    dot = Digraph(comment="Huffman Tree")

    def add_nodes_edges(node: Node, parent_id=None, symbol=None):
        node_id = id(node)
        label = f"{node.target}\n{node.count}" if node.target else str(node.count)
        shape = "ellipse" if node.target else "box"
        dot.node(name=str(node_id), label=label, shape=shape)

        if parent_id is not None and symbol is not None:
            dot.edge(str(parent_id), str(node_id), label=symbol)

        for i, child in enumerate(node.children):
            add_nodes_edges(child, node_id, symbols[i])

    # Add metadata to the graph
    metadata = (
        f"Count Dict: {count_dict}\nSymbols: {symbols}\n"
        f"Branch Points: {num_branch_points}\nPadding: {num_padding}"
    )
    dot.attr(label=metadata)
    dot.attr(fontsize="10")

    add_nodes_edges(root)
    dot.render(output_path, format="png", cleanup=True)


# Example usage:
if __name__ == "__main__":
    output_dir = "manual_tests/output/random_trees"
    os.makedirs(output_dir, exist_ok=True)

    test_random_trees(num_tests=10, output_dir=output_dir)
    print("Random tree visualizations generated.")
