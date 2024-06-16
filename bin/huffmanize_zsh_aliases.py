#!/usr/bin/env python3

import sys
from huffman_arpeggio.utils import generate_count_dict, generate_zsh_aliases
from huffman_arpeggio.core import (
    build_huffman_tree,
    generate_encoding_map_with_count,
)


def main():
    # Read lines from stdin
    input_lines = sys.stdin.read().strip().split("\n")

    # Generate the count dictionary
    count_dict = generate_count_dict(input_lines)

    # Define the alphabet for encoding
    alphabet = [
        "j",
        "f",
        "k",
        "d",
        "l",
        "s",
    ]

    # Build the Huffman tree
    root = build_huffman_tree(count_dict, alphabet)

    # Generate the encoding map
    encoding_map = generate_encoding_map_with_count(root, alphabet, count_dict)

    # Sort the encoding map by descending count
    sorted_encoding_map = dict(
        sorted(encoding_map.items(), key=lambda item: item[1][1], reverse=True)
    )

    # Generate Zsh aliases
    aliases = generate_zsh_aliases(sorted_encoding_map)

    # Output the aliases to stdout
    for alias in aliases:
        print(alias)


if __name__ == "__main__":
    main()
