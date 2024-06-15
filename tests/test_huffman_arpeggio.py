import os
import unittest
import pandas as pd
from huffman_arpeggio.__main__ import main

class TestHuffmanArpeggio(unittest.TestCase):
    def setUp(self):
        self.input_file = 'tests/data/playstation-qwerty-wikipedia-example-input.csv'
        self.expected_output_file = 'tests/data/playstation-qwerty-wikipedia-example-output.csv'
        self.output_file = 'tests/data/tmp_output.csv'
        self.sequence_col = 'keyswitch'
        self.target_col = 'freq'

    def test_end_to_end(self):
        # Run the main function to generate the output
        main(self.input_file, self.output_file, self.sequence_col, self.target_col)
        
        # Load the generated output and the expected output
        generated_output = pd.read_csv(self.output_file)
        expected_output = pd.read_csv(self.expected_output_file)
        
        # Compare the two dataframes
        pd.testing.assert_frame_equal(generated_output, expected_output)
        
        # Clean up the temporary file
        os.remove(self.output_file)

if __name__ == '__main__':
    unittest.main()
