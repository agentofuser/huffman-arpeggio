#!/usr/bin/env python3

import sys
import subprocess
import logging
import shlex
from typing import Dict, Tuple, List
from huffman_arpeggio.utils import generate_count_dict
from huffman_arpeggio.core import (
    build_huffman_tree,
    generate_encoding_map_with_count,
)


def is_alias_conflict(alias: str) -> bool:
    """
    Check if the alias conflicts with an existing command in the PATH, Zsh
    functions, aliases, shell builtins, or keywords.

    :param alias: The alias to check.
    :return: True if there is a conflict, False otherwise.
    """
    logger = logging.getLogger(__name__)

    result = subprocess.run(
        ["zsh", "-i", "-c", f"type {shlex.quote(alias)}"],
        capture_output=True,
        text=True,
    )
    if result.stdout.strip().endswith("not found"):
        return False

    logger.info(f"Shell conflict: {result.stdout.strip()}")
    return True


def sanitize_input_lines(input_lines: List[str]) -> List[str]:
    """
    Sanitize input lines to remove trailing backslashes and any other unwanted
    characters.

    :param input_lines: The list of input command lines.
    :return: The sanitized list of input command lines.
    """
    sanitized_lines = []
    for line in input_lines:
        sanitized_line = line.rstrip("\\").strip()
        sanitized_lines.append(sanitized_line)
    return sanitized_lines


def filter_commands(
    count_dict: Dict[str, int],
    alphabet: List[str],
) -> Dict[Tuple[str, ...], Tuple[str, int]]:
    logger = logging.getLogger(__name__)
    logger.debug(f"Initial count_dict: {count_dict}")

    iteration = 0
    previous_name_conflicts = {}
    valid_aliases = {}

    while True:
        iteration += 1
        logger.info(
            f"Iteration: {iteration}, count_dict size: {len(count_dict)}"
        )

        # Build the Huffman tree
        root = build_huffman_tree(count_dict, alphabet)

        # Generate the encoding map
        encoding_map = generate_encoding_map_with_count(
            root, alphabet, count_dict
        )

        logger.debug(f"Encoding map: {encoding_map}")

        # DEBUG: figure out what's happening to `('j',)` which shows up in the
        # first iteration encoding map, then disappears in the second iteration,
        # and generates no "Pruned" log message.
        # The _target_ is still assigned a different alias path/name, but the
        # 'j' is _not_ a conflict, and it's never reused, even as length-2
        # aliases are created:
        # Iteration: 1, count_dict size: 11
        # Encoding map: {('j',): ('atuin history list --format="{command}" | poetry run huffmanize-zsh-aliases', 7), ('f',): ('gd', 8), ('k',): ('gs', 10), ('d',): ('vz', 11), ('l',): ('atuin history list --format="{command}" | poetry run huffmanize-zsh-aliases --verbose=info', 17), ('s', 'j'): ('poetry run local-harps', 4), ('s', 'f'): ('ck', 4), ('s', 'k'): ('da', 5), ('s', 'd'): ('poetry run scripts/run_all.sh', 6), ('s', 'l'): ('l', 6), ('s', 's'): ('poetry run python', 7)}
        # Pruned alias (poor ROI): ('f',), target: gd
        # Pruned alias (poor ROI): ('k',), target: gs
        # Pruned alias (poor ROI): ('d',), target: vz
        # Shell conflict: l is an alias for eza --long --classify --header --accessed --all --group-directories-first
        # Pruned alias (conflict): ('l',), target: atuin history list --format="{command}" | poetry run huffmanize-zsh-aliases --verbose=info
        # Shell conflict: l is an alias for eza --long --classify --header --accessed --all --group-directories-first
        # Pruned alias (poor ROI): ('s', 'f'), target: ck
        # Pruned alias (poor ROI): ('s', 'k'), target: da
        # Pruned alias (poor ROI): ('s', 'l'), target: l
        # New count_dict size: 5
        # Iteration: 2, count_dict size: 5
        # Encoding map: {('f',): ('poetry run local-harps', 4), ('k',): ('poetry run scripts/run_all.sh', 6), ('d',): ('atuin history list --format="{command}" | poetry run huffmanize-zsh-aliases', 7), ('l',): ('poetry run python', 7), ('s',): ('atuin history list --format="{command}" | poetry run huffmanize-zsh-aliases --verbose=info', 17)}

        # Clone the encoding map to update it without affecting the iteration
        updated_encoding_map = encoding_map.copy()

        # Check and replace previously invalid entries with valid ones
        for original_alias, (
            valid_alias,
            target,
            count,
        ) in valid_aliases.items():
            if (
                original_alias in updated_encoding_map
                and updated_encoding_map[original_alias][0] == target
            ):
                updated_encoding_map[valid_alias] = (target, count)
                del updated_encoding_map[original_alias]

        # Filter aliases
        pruned = False
        new_count_dict = {}
        for alias_path, (target, count) in encoding_map.items():
            # Check if replaced by a valid alias
            if alias_path in valid_aliases:
                alias_path = valid_aliases[alias_path][0]

            # Check for poor ROI
            if len(alias_path) >= len(target) / 2:
                pruned = True
                logger.info(
                    f"Pruned alias (poor ROI): {alias_path}, target: {target}"
                )
                continue

            # Check for conflicts
            if alias_path in previous_name_conflicts or is_alias_conflict(
                "".join(alias_path)
            ):
                pruned = True
                previous_name_conflicts[alias_path] = target
                logger.info(
                    f"Pruned alias (conflict): {alias_path}, target: {target}"
                )

                # Augment the alias path to avoid conflict
                augmented_alias_path = alias_path
                augment_index = 0
                while is_alias_conflict("".join(augmented_alias_path)):
                    augmented_alias_path += (alphabet[augment_index],)
                    augment_index = (augment_index + 1) % len(alphabet)
                if len(augmented_alias_path) < len(target) / 2:
                    new_count_dict[target] = count_dict.get(target, 0)
                    valid_aliases[alias_path] = (
                        augmented_alias_path,
                        target,
                        count,
                    )
                continue

            # No pruning needed, add to new count_dict
            new_count_dict[target] = count_dict.get(target, 0)

        if not pruned:
            logger.info("No pruning needed, returning encoding map")
            logger.debug(f"Final encoding map: {updated_encoding_map}")
            return dict(
                sorted(
                    updated_encoding_map.items(),
                    key=lambda item: item[1][1],
                    reverse=True,
                )
            )
        elif not new_count_dict:
            logger.info("No valid commands left, returning empty dictionary")
            return {}
        else:
            count_dict = new_count_dict
            logger.info(f"New count_dict size: {len(count_dict)}")


def main():
    # Setup logging
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    logger = logging.getLogger(__name__)

    # Parse verbosity level
    if "--verbose=debug" in sys.argv:
        logger.setLevel(logging.DEBUG)
    elif "--verbose=info" in sys.argv:
        logger.setLevel(logging.INFO)
    elif "--verbose" in sys.argv:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    # Read lines from stdin
    input_lines = sys.stdin.read().strip().split("\n")
    logger.debug(f"Input lines: {input_lines}")

    # Sanitize input lines
    input_lines = sanitize_input_lines(input_lines)
    logger.debug(f"Sanitized input lines: {input_lines}")

    # Generate the count dictionary
    count_dict = generate_count_dict(input_lines)

    # Filter out commands with count < 4
    count_dict = {
        cmd: count for cmd, count in count_dict.items() if count >= 4
    }
    logger.debug(f"Filtered count_dict: {count_dict}")

    # Define the alphabet for encoding
    alphabet = ["j", "f", "k", "d", "l", "s"]

    # Filter commands to get the final encoding map
    final_encoding_map = filter_commands(count_dict, alphabet)

    if not final_encoding_map:
        return

    logger.debug(f"Final encoding map: {final_encoding_map}")

    # Generate the final Zsh aliases from the encoding map
    for alias_path, (target, count) in final_encoding_map.items():
        alias_name = "".join(alias_path)
        print(f"alias {alias_name}='{target}'")


if __name__ == "__main__":
    main()
