#!/usr/bin/env python3

import sys
import shutil
import subprocess
import logging
import shlex
from typing import Dict, Tuple
from huffman_arpeggio.utils import generate_count_dict, generate_zsh_aliases
from huffman_arpeggio.core import (
    build_huffman_tree,
    generate_encoding_map_with_count,
)


def is_alias_conflict(alias: str) -> bool:
    """
    Check if the alias conflicts with an existing command in the PATH or with Zsh functions and aliases.

    :param alias: The alias to check.
    :return: True if there is a conflict, False otherwise.
    """
    logger = logging.getLogger(__name__)
    # Check PATH
    if shutil.which(alias) is not None:
        logger.info(f"Zsh PATH conflict: {repr(alias)}")
        return True

    # Check Zsh functions
    result = subprocess.run(
        ["zsh", "-c", f"whence -w {shlex.quote(alias)}"],
        capture_output=True,
        text=True,
    )
    if result.stdout.strip() != f"{alias}: none":
        logger.info(f"Zsh function conflict: {result.stdout.strip()}")
        return True

    # Check existing aliases
    result = subprocess.run(
        ["zsh", "-c", f"alias {shlex.quote(alias)}"],
        capture_output=True,
        text=True,
    )
    if result.stdout.strip():
        logger.info(f"Existing alias conflict: {result.stdout.strip()}")
        return True

    return False


def filter_commands(
    count_dict: Dict[str, int], alphabet: str
) -> Dict[str, int]:
    """
    Filter commands that result in suboptimal or conflicting aliases.

    :param count_dict: The initial count dictionary.
    :param alphabet: The alphabet used for generating aliases.
    :return: The pruned count dictionary.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"Initial count_dict: {count_dict}")

    iteration = 0

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

        # Sort the encoding map by descending count
        sorted_encoding_map = dict(
            sorted(
                encoding_map.items(), key=lambda item: item[1][1], reverse=True
            )
        )

        # Generate Zsh aliases
        candidate_aliases = generate_zsh_aliases(sorted_encoding_map)

        logger.debug(f"Generated aliases: {candidate_aliases}")

        # Filter aliases
        pruned = False
        new_count_dict = {}
        for alias_name, target in candidate_aliases.items():
            # logger.info(f"Checking alias: {repr(alias_name)}")
            # logger.info(f"Target: {repr(target)}")

            if len(alias_name) >= len(target) / 2 or is_alias_conflict(
                alias_name
            ):
                pruned = True
                logger.info(
                    f"Pruned alias: {repr(alias_name)}, target: {repr(target)}"
                )
            else:
                new_count_dict[target] = count_dict.get(target, 0)

        if not pruned:
            logger.info(
                f"No pruning needed, returning count_dict: {new_count_dict}"
            )
            return new_count_dict
        elif not new_count_dict:
            logger.info("No valid commands left, returning empty dictionary")
            return (
                {}
            )  # Return an empty dictionary if no valid commands are left
        else:
            count_dict = new_count_dict
            logger.info(f"New count_dict size: {len(count_dict)}")


def main():
    # Setup logging
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    logger = logging.getLogger(__name__)

    # Parse verbosity level
    log_level = "info"
    if "--verbose=debug" in sys.argv:
        log_level = "debug"
        logger.setLevel(logging.DEBUG)
    elif "--verbose=info" in sys.argv:
        logger.setLevel(logging.INFO)
        log_level = "info"
    elif "--verbose" in sys.argv:
        log_level = "info"
        logger.setLevel(logging.INFO)
    else:
        log_level = None
        logger.setLevel(logging.WARNING)

    # Read lines from stdin
    input_lines = sys.stdin.read().strip().split("\n")

    logger.debug(f"Input lines: {input_lines}")

    # Generate the count dictionary
    count_dict = generate_count_dict(input_lines)

    logger.debug(f"Generated count_dict: {count_dict}")

    # Define the alphabet for encoding
    alphabet = ["j", "f", "k", "d", "l", "s"]

    # Filter commands to get the pruned count dictionary
    pruned_count_dict = filter_commands(count_dict, alphabet)

    print("HELLO")

    if not pruned_count_dict:
        return

    logger.debug(f"Pruned count_dict: {pruned_count_dict}")

    # Build the final Huffman tree
    root = build_huffman_tree(pruned_count_dict, alphabet)

    # Generate the final encoding map
    encoding_map = generate_encoding_map_with_count(
        root, alphabet, pruned_count_dict
    )

    logger.debug(f"Final encoding map: {encoding_map}")

    # Sort the final encoding map by descending count
    sorted_encoding_map = dict(
        sorted(encoding_map.items(), key=lambda item: item[1][1], reverse=True)
    )

    # Generate the final Zsh aliases
    aliases = generate_zsh_aliases(sorted_encoding_map)

    # Output the final aliases to stdout
    for alias in aliases:
        print(alias)


if __name__ == "__main__":
    main()
