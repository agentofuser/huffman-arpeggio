# huffman_arpeggio/core.py

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
