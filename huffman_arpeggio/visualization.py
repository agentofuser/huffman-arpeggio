from graphviz import Digraph
from huffman_arpeggio.core import Node


def visualize_huffman_tree(root: Node, output_path: str):
    """
    Visualize the Huffman tree using Graphviz.

    :param root: The root of the Huffman tree.
    :param output_path: The path to save the output visualization file.
    """
    dot = Digraph(comment="Huffman Tree")

    def add_nodes_edges(node: Node, parent_id=None):
        node_id = id(node)
        label = f"{node.target}\n{node.count}" if node.target else str(node.count)
        dot.node(name=str(node_id), label=label)

        if parent_id is not None:
            dot.edge(str(parent_id), str(node_id))

        for child in node.children:
            add_nodes_edges(child, node_id)

    add_nodes_edges(root)
    dot.render(output_path, format="png", cleanup=True)
