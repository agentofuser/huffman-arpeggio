import os
import pytest
import pandas as pd
from huffman_arpeggio.core import build_huffman_tree, generate_encoding_map_with_count
from huffman_arpeggio.utils import load_count_dict, save_encoding_map_with_count


@pytest.fixture
def test_data():
    input_file = "tests/data/playstation-qwerty-wikipedia-example-input.csv"
    expected_output_file = "tests/data/playstation-qwerty-wikipedia-example-output.csv"
    output_file = "tests/data/tmp_output.csv"
    target_col = "keyswitch"
    count_col = "count"

    yield {
        "input_file": input_file,
        "expected_output_file": expected_output_file,
        "output_file": output_file,
        "target_col": target_col,
        "count_col": count_col,
    }

    if os.path.exists(output_file):
        os.remove(output_file)


def test_end_to_end(test_data):
    # Load count dictionary
    count_dict = load_count_dict(
        test_data["input_file"], test_data["target_col"], test_data["count_col"]
    )

    # Define the alphabet
    alphabet = ["X", "O", "□", "∆", "⬇️", "⬆️", "⬅️", "➡️"]

    # Build Huffman tree
    root = build_huffman_tree(count_dict, alphabet)

    # Generate encoding map
    encoding_map_with_count = generate_encoding_map_with_count(
        root, alphabet, count_dict
    )

    # Save the encoding map to the output file
    save_encoding_map_with_count(encoding_map_with_count, test_data["output_file"])

    # Load the generated output and the expected output
    generated_output = pd.read_csv(test_data["output_file"])
    expected_output = pd.read_csv(test_data["expected_output_file"])

    # Compare the two dataframes
    pd.testing.assert_frame_equal(generated_output, expected_output)
