import sys
import pandas as pd
from heapq import heappush, heappop, heapify
import math

class Node:
    def __init__(self, count, character=None, children=None):
        self.count = count
        self.character = character
        self.children = children if children is not None else []

    def __lt__(self, other):
        return self.count < other.count

    def __repr__(self):
        return f"Node(count={self.count}, character={self.character}, children={self.children})"

def calculate_padding(num_elements, num_branches):
    num_branch_points = math.ceil((num_elements - 1) / (num_branches - 1))
    num_padding = 1 + (num_branches - 1) * num_branch_points - num_elements
    return num_branch_points, num_padding

def merge_nodes(nodes, num_branches):
    heapify(nodes)
    
    while len(nodes) > 1:
        merged_count = 0
        merged_children = []
        
        for _ in range(min(num_branches, len(nodes))):
            node = heappop(nodes)
            merged_count += node.count
            merged_children.append(node)
        
        merged_node = Node(merged_count, None, merged_children)
        heappush(nodes, merged_node)

    return nodes[0] if nodes else None

def build_huffman_tree(count_dict, alphabet):
    num_elements = len(count_dict)
    num_branches = len(alphabet)
    
    num_branch_points, num_padding = calculate_padding(num_elements, num_branches)
    
    nodes = [Node(count, char) for char, count in count_dict.items()]
    
    for _ in range(num_padding):
        nodes.append(Node(0, None))
    
    root = merge_nodes(nodes, num_branches)
    
    return root

def generate_encoding_map_with_count(root, alphabet, count_dict):
    def traverse(node, path, encoding_map):
        if node.character is not None:
            encoding_map[tuple(path)] = (node.character, count_dict[node.character])
        for i, child in enumerate(node.children):
            traverse(child, path + [alphabet[i]], encoding_map)
    
    encoding_map = {}
    traverse(root, [], encoding_map)
    return encoding_map

def load_count_dict(file_path, target_col, count_col):
    df = pd.read_csv(file_path)
    return df.set_index(target_col)[count_col].to_dict()

def save_encoding_map_with_count(encoding_map_with_count, output_path):
    encoding_map_data_with_count = [{'sequence': ' '.join(path), 'target': target, 'count': count} for path, (target, count) in encoding_map_with_count.items()]
    encoding_map_df_with_count = pd.DataFrame(encoding_map_data_with_count)
    encoding_map_df_with_count.sort_values(by='count', ascending=False, inplace=True)
    encoding_map_df_with_count.reset_index(drop=True, inplace=True)
    encoding_map_df_with_count.to_csv(output_path, index=False)

def main(file_path, output_path, target_col, count_col):
    count_dict = load_count_dict(file_path, target_col, count_col)
    alphabet = ['X', 'O', '□', '∆', '⬇️', '⬆️', '⬅️', '➡️']
    root = build_huffman_tree(count_dict, alphabet)
    encoding_map_with_count = generate_encoding_map_with_count(root, alphabet, count_dict)
    save_encoding_map_with_count(encoding_map_with_count, output_path)
    print(f"Encoding map with counts has been written to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python -m huffman_arpeggio <input_file_path> <output_file_path> <target_col> <count_col>")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    target_col = sys.argv[3]
    count_col = sys.argv[4]
    main(input_file_path, output_file_path, target_col, count_col)
