#!/usr/bin/env python3

import subprocess
import os
from huffman_arpeggio.utils import generate_count_dict
from huffman_arpeggio.core import (
    build_huffman_tree,
    generate_encoding_map_with_count,
)
from bin.huffmanize_zsh_aliases import (
    is_alias_conflict,
    sanitize_input_lines,
    filter_commands,
)


def get_history():
    result = subprocess.run(
        ["atuin", "history", "list", "--format", "{command}", "--cwd"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip().split("\n")


def generate_aliases(history, alphabet, min_count=4):
    count_dict = generate_count_dict(history)
    count_dict = {
        cmd: count for cmd, count in count_dict.items() if count >= min_count
    }

    if not count_dict:
        return {}

    final_encoding_map = filter_commands(count_dict, alphabet)
    aliases = {
        "".join(alias_path): target
        for alias_path, (target, _) in final_encoding_map.items()
    }
    return aliases


def print_aliases(aliases):
    print("Generated aliases:")
    for alias, command in aliases.items():
        print(f"alias {alias}='{command}'")


def main():
    alphabet = ["j", "f", "k", "d", "l", "s"]
    history = get_history()
    sanitized_history = sanitize_input_lines(history)
    aliases = generate_aliases(sanitized_history, alphabet)

    os.makedirs(".keykapp", exist_ok=True)
    with open(".keykapp/local_harps.sh", "w") as f:
        for alias, command in aliases.items():
            f.write(f"alias {alias}='{command}'\n")

    print_aliases(aliases)


if __name__ == "__main__":
    main()
