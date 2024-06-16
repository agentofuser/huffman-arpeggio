import pandas as pd
from typing import Dict, Tuple


def load_count_dict(file_path: str, target_col: str, count_col: str) -> Dict[str, int]:
    """
    Load the count dictionary from a CSV file.

    :param file_path: Path to the CSV file.
    :param target_col: The column containing the targets.
    :param count_col: The column containing the counts.
    :return: A dictionary mapping targets to their counts.
    """
    df = pd.read_csv(file_path)
    return df.set_index(target_col)[count_col].to_dict()


def save_encoding_map_with_count(
    encoding_map_with_count: Dict[Tuple[str, ...], Tuple[str, int]], output_path: str
):
    """
    Save the encoding map with counts to a CSV file.

    :param encoding_map_with_count: The encoding map with counts.
    :param output_path: Path to the output CSV file.
    """
    encoding_map_data_with_count = [
        {"sequence": " ".join(path), "target": target, "count": count}
        for path, (target, count) in encoding_map_with_count.items()
    ]
    encoding_map_df_with_count = pd.DataFrame(encoding_map_data_with_count)
    encoding_map_df_with_count.sort_values(by="count", ascending=False, inplace=True)
    encoding_map_df_with_count.reset_index(drop=True, inplace=True)
    encoding_map_df_with_count.to_csv(output_path, index=False)
