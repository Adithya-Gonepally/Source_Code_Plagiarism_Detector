import pandas as pd
import os

def load_code_database(language):
    filepath = {
        "Python": os.path.join("..", "database", "python_database.csv"),
        "C": os.path.join("..", "database", "c_database.csv")
    }[language]

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not find the file: {filepath}")

    return pd.read_csv(filepath, on_bad_lines='skip')



def get_code_samples(language):
    df = load_code_database(language)
    df.columns = df.columns.str.strip()  # Trim whitespace from column names

    # Verify that the required columns exist
    if 'file_name' not in df.columns or 'content' not in df.columns:
        raise KeyError("Required columns 'file_name' and/or 'content' not found in the database.")

    filenames = df['file_name'].tolist()
    code_samples = [str(content) for content in df['content'].tolist()]
    return filenames, code_samples
