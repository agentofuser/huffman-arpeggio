# huffman_arpeggio/utils.py

import pandas as pd

def load_count_dict(file_path, target_col, count_col):
    df = pd.read_csv(file_path)
    return df.set_index(target_col)[count_col].to_dict()

def save_encoding_map_with_count(encoding_map_with_count, output_path):
    encoding_map_data_with_count = [{'sequence': ' '.join(path), 'target': target, 'count': count} for path, (target, count) in encoding_map_with_count.items()]
    encoding_map_df_with_count = pd.DataFrame(encoding_map_data_with_count)
    encoding_map_df_with_count.sort_values(by='count', ascending=False, inplace=True)
    encoding_map_df_with_count.reset_index(drop=True, inplace=True)
    encoding_map_df_with_count.to_csv(output_path, index=False)
