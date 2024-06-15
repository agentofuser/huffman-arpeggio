import sys
import pandas as pd
from heapq import heappush, heappop, heapify
import math

class Node:
    def __init__(self, frequency, character=None, children=None):
        self.frequency = frequency
        self.character = character
        self.children = children if children is not None else []

    def __lt__(self, other):
        return self.frequency < other.frequency

    def __repr__(self):
        return f"Node(frequency={self.frequency}, character={self.character}, children={self.children})"

def calculate_padding(num_elements, num_branches):
    num_branch_points = math.ceil((num_elements - 1) / (num_branches - 1))
    num_padding = 1 + (num_branches - 1) * num_branch_points - num_elements
    return num_branch_points, num_padding

def merge_nodes(nodes, num_branches):
    heapify(nodes)
    
    while len(nodes) > 1:
        merged_frequency = 0
        merged_children = []
        
        for _ in range(min(num_branches, len(nodes))):
            node = heappop(nodes)
            merged_frequency += node.frequency
            merged_children.append(node)
        
        merged_node = Node(merged_frequency, None, merged_children)
        heappush(nodes, merged_node)

    return nodes[0] if nodes else None

def build_huffman_tree(frequency_dict, alphabet):
    num_elements = len(frequency_dict)
    num_branches = len(alphabet)
    
    num_branch_points, num_padding = calculate_padding(num_elements, num_branches)
    
    nodes = [Node(frequency, char) for char, frequency in frequency_dict.items()]
    
    for _ in range(num_padding):
        nodes.append(Node(0, None))
    
    root = merge_nodes(nodes, num_branches)
    
    return root

def generate_encoding_map_with_freq(root, alphabet, frequency_dict):
    def traverse(node, path, encoding_map):
        if node.character is not None:
            encoding_map[tuple(path)] = (node.character, frequency_dict[node.character])
        for i, child in enumerate(node.children):
            traverse(child, path + [alphabet[i]], encoding_map)
    
    encoding_map = {}
    traverse(root, [], encoding_map)
    return encoding_map

def main(file_path):
    df = pd.read_csv(file_path)
    frequency_dict = df.set_index('keyswitch')['freq'].to_dict()

    alphabet = ['X', 'O', '□', '∆', '⬇️', '⬆️', '⬅️', '➡️']

    root = build_huffman_tree(frequency_dict, alphabet)
    encoding_map_with_freq = generate_encoding_map_with_freq(root, alphabet, frequency_dict)

    encoding_map_data_with_freq = [{'sequence': ' '.join(path), 'keyswitch': keyswitch, 'frequency': freq} for path, (keyswitch, freq) in encoding_map_with_freq.items()]

    encoding_map_df_with_freq = pd.DataFrame(encoding_map_data_with_freq)
    encoding_map_df_with_freq.sort_values(by='frequency', inplace=True)
    encoding_map_df_with_freq.reset_index(drop=True, inplace=True)

    print(encoding_map_df_with_freq)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python huffmanizer.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    main(file_path)
