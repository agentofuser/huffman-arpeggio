import os
import unittest
import pandas as pd
from huffman_arpeggio.core import build_huffman_tree, generate_encoding_map_with_count
from huffman_arpeggio.utils import load_count_dict, save_encoding_map_with_count

class TestHuffmanArpeggio(unittest.TestCase):
    def setUp(self):
        self.input_file = 'tests/data/playstation-qwerty-wikipedia-example-input.csv'
        self.expected_output_file = 'tests/data/playstation-qwerty-wikipedia-example-output.csv'
        self.output_file = 'tests/data/tmp_output.csv'
        self.target_col = 'keyswitch'
        self.count_col = 'count'

    def test_end_to_end(self):
        # Load count dictionary
        count_dict = load_count_dict(self.input_file, self.target_col, self.count_col)
        
        # Define the alphabet
        alphabet = ['X', 'O', '□', '∆', '⬇️', '⬆️', '⬅️', '➡️']
        
        # Build Huffman tree
        root = build_huffman_tree(count_dict, alphabet)
        
        # Generate encoding map
        encoding_map_with_count = generate_encoding_map_with_count(root, alphabet, count_dict)
        
        # Save the encoding map to the output file
        save_encoding_map_with_count(encoding_map_with_count, self.output_file)
        
        # Load the generated output and the expected output
        generated_output = pd.read_csv(self.output_file)
        expected_output = pd.read_csv(self.expected_output_file)
        
        # Compare the two dataframes
        pd.testing.assert_frame_equal(generated_output, expected_output)
        
        # Clean up the temporary file
        os.remove(self.output_file)

if __name__ == '__main__':
    unittest.main()
