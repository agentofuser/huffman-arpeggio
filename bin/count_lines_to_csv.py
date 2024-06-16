#!/usr/bin/env python3

import sys
import csv
from huffman_arpeggio.utils import generate_count_dict


def main():
    # Read lines from stdin
    input_lines = sys.stdin.read().strip().split("\n")

    # Generate the count dictionary
    count_dict = generate_count_dict(input_lines)

    # Sort the dictionary by descending count
    sorted_count_list = sorted(
        count_dict.items(), key=lambda item: item[1], reverse=True
    )

    # Output CSV to stdout
    writer = csv.writer(sys.stdout)
    writer.writerow(["target", "count"])
    for target, count in sorted_count_list:
        writer.writerow([target, count])


if __name__ == "__main__":
    main()
